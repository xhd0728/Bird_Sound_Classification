# -*- encoding:utf-8 -*-
"""model module"""
import os
import re
from pathlib import Path

import librosa
import numpy as np
import timm
import torch
import torchaudio as ta
from torch import nn
from torch.nn import functional as F
from torch.nn.parameter import Parameter

from config.model import NAME_CN_LIST, NAME_EN_LIST, MODEL_PATH


def gem(x, p=3, eps=1e-6):
    return F.avg_pool2d(x.clamp(min=eps).pow(p), (x.size(-2), x.size(-1))).pow(1.0 / p)


class GeM(nn.Module):
    def __init__(self, p=3, eps=1e-6):
        super(GeM, self).__init__()
        self.p = Parameter(torch.ones(1) * p)
        self.eps = eps

    def forward(self, x):
        ret = gem(x, p=self.p, eps=self.eps)
        return ret

    def __repr__(self):
        return (
                self.__class__.__name__
                + "("
                + "p="
                + "{:.4f}".format(self.p.data.tolist()[0])
                + ", "
                + "eps="
                + str(self.eps)
                + ")"
        )


class TimmClassifier(nn.Module):
    def __init__(self, encoder: str,
                 pretrained=True,
                 classes=21,
                 enable_masking=False,
                 **kwargs
                 ):
        super().__init__()

        # print(f"initing CLS features model {kwargs['duration']} duration...")

        mel_config = kwargs['mel_config']
        self.mel_spec = ta.transforms.MelSpectrogram(
            sample_rate=mel_config['sample_rate'],
            n_fft=mel_config['window_size'],
            win_length=mel_config['window_size'],
            hop_length=mel_config['hop_size'],
            f_min=mel_config['fmin'],
            f_max=mel_config['fmax'],
            pad=0,
            n_mels=mel_config['mel_bins'],
            power=mel_config['power'],
            normalized=False,
        )

        self.amplitude_to_db = ta.transforms.AmplitudeToDB(top_db=mel_config['top_db'])
        self.wav2img = torch.nn.Sequential(self.mel_spec, self.amplitude_to_db).cuda()
        self.enable_masking = enable_masking
        if enable_masking:
            self.freq_mask = ta.transforms.FrequencyMasking(24, iid_masks=True)
            self.time_mask = ta.transforms.TimeMasking(64, iid_masks=True)

        base_model = timm.create_model(
            encoder,
            pretrained=pretrained,
            num_classes=0,
            global_pool="",
            **kwargs['backbone_params']
        )
        if "efficientnet" in encoder:
            backbone_out = base_model.num_features
        else:
            backbone_out = base_model.feature_info[-1]["num_chs"]

        self.encoder = base_model

        self.gem = GeM(p=3, eps=1e-6)
        self.head1 = nn.Linear(backbone_out, classes, bias=True)

        # 30 seconds -> 5 seconds
        wav_crop_len = kwargs["duration"]
        self.factor = int(wav_crop_len / 5.0)

    # TODO: optional normalization of mel
    def forward(self, x, is_test=False):
        if not is_test:
            x = x[:, 0, :]  # bs, ch, time -> bs, time
            bs, time = x.shape
            x = x.reshape(bs * self.factor, time // self.factor)
        else:
            # only 5 seconds infer...
            x = x  # bs, ch, time -> bs, time

        with torch.cuda.amp.autocast(enabled=False):
            x = self.wav2img(x)  # bs, ch, mel, time
            x = (x + 80) / 80

        if self.training and self.enable_masking:
            x = self.freq_mask(x)
            x = self.time_mask(x)

        x = x.permute(0, 2, 1)
        x = x[:, None, :, :]

        x = self.encoder(x)
        if self.training:
            b, c, t, f = x.shape
            x = x.permute(0, 2, 1, 3)
            x = x.reshape(b // self.factor, self.factor * t, c, f)
            x = x.permute(0, 2, 1, 3)

        x = self.gem(x)
        x = x[:, :, 0, 0]
        logit = self.head1(x)
        return {"logit": logit}


"""load model"""


def load_one(filename, sr):
    # try:
    wav, sr = librosa.load(filename, sr=sr)
    return torch.tensor(wav).unsqueeze(0).cuda()


def softmax(x):
    # 将输入向量减去最大值，避免指数太大导致计算溢出
    x_max = np.max(x)
    exp_x = np.exp(x - x_max)
    # 对指数进行归一化
    return exp_x / np.sum(exp_x)


def find_max_index(arr):
    max_index = np.argmax(arr)
    return max_index


def audio_classifier(audio_path):
    encoder_params = {
        "encoder": "efficientnet_b4",
        "duration": 20,
        "val_duration": 10,
        "classes": 264,
        "backbone_params": {
            "in_chans": 1,
            "drop_path_rate": 0.2,
            "drop_rate": 0.5
        },
        "mel_config": {"sample_rate": 32000,
                       "window_size": 1024,
                       "hop_size": 320,
                       "fmin": 50,
                       "fmax": 14000,
                       "mel_bins": 128,
                       "power": 2,
                       "top_db": None}
    }
    model = TimmClassifier(**encoder_params)
    model = model.cuda()
    model.eval()

    pth_path = MODEL_PATH

    checkpoint_path = pth_path
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    state_dict = checkpoint["state_dict"]
    state_dict = {re.sub("^module.", "", k): w for k, w in state_dict.items()}
    orig_state_dict = model.state_dict()
    mismatched_keys = []
    for k, v in state_dict.items():
        ori_size = orig_state_dict[k].size() if k in orig_state_dict else None
        if v.size() != ori_size:
            print("SKIPPING!!! Shape of {} changed from {} to {}".format(k, v.size(), ori_size))
            mismatched_keys.append(k)
    for k in mismatched_keys:
        del state_dict[k]
    model.load_state_dict(state_dict, strict=False)
    print("=> loaded checkpoint '{}' (epoch {})".format(checkpoint_path, checkpoint['epoch']))

    filename = audio_path
    sr = 16000

    wav = load_one(filename, sr)
    outs = model(wav, is_test=True)

    sample_path = os.path.join(Path(__file__).resolve().parent, "sample_submission.csv")

    outs = softmax(outs['logit'].sigmoid().cpu().detach().numpy())[0]
    # classes = pd.read_csv(sample_path).columns[1:]
    classes = NAME_CN_LIST
    classes_en = NAME_EN_LIST

    # select the first ten indices
    sorted_arr = sorted(range(len(outs)), key=lambda i: outs[i], reverse=True)

    # select the first ten indices
    top_ten_indices = sorted_arr[:10]

    value = []
    category = []
    category_en = []
    for index in top_ten_indices:
        value.append(10000 * (outs[index] - 0.4))
        category_en.append(classes_en[index])
        category.append(classes[index])
    value = softmax(value)
    return {
        "category_cn": category,
        "category_en": category_en,
        "value": value
    }


"""音频文件路径"""


def select_classic(audio_path):
    return audio_classifier(audio_path)
