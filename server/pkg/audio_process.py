import base64
import os
from pathlib import Path

import librosa.display
import librosa.feature
import matplotlib.pyplot as plt
import numpy
import numpy as np
from PIL import Image

AUDIO_EXAMPLE_PATH = os.path.join(Path(__file__).resolve().parent.parent, "media", "example_audio")
SAVE_IMAGE_PATH = os.path.join(Path(__file__).resolve().parent.parent, "media", "save_image")
UPLOAD_AUDIO_PATH = os.path.join(Path(__file__).resolve().parent.parent, "media", "upload_audio")


def get_audio_b64(audio_name) -> dict:
    if not audio_name:
        return {
            "success": False,
            "error": "未声明音频名称"
        }
    file_path = os.path.join(UPLOAD_AUDIO_PATH, audio_name)
    print(file_path)
    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": "音频文件不存在"
        }
    try:
        with open(file_path, "rb") as f:
            encoded_file = base64.b64encode(f.read())
            return {
                "success": True,
                "data": encoded_file.decode("utf-8")
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_audio_spectrogram(audio_name) -> dict:
    file_path = os.path.join(UPLOAD_AUDIO_PATH, audio_name)
    print(file_path)
    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": "音频文件不存在"
        }

    try:
        audio, sr = librosa.load(file_path)
        mel_spect = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=3200, hop_length=80)
        mel_spect1 = librosa.power_to_db(mel_spect, ref=numpy.max)

        np.random.seed(0)
        # 生成长度为 N 的白噪声信号
        noise = np.random.normal(0, 1, size=mel_spect1.shape)

        mel_spect1 = mel_spect1 + 0.05 * noise * np.abs(mel_spect1)

        librosa.display.specshow(mel_spect1, y_axis='mel', fmax=8000, x_axis='time')
        # 显示图像
        plt.axis('off')  # 去坐标轴
        plt.xticks([])  # 去刻度
        plt.yticks([])  # 去刻度

        (file_prefix, file_suffix) = os.path.splitext(audio_name)
        image_path = os.path.join(SAVE_IMAGE_PATH, f"{file_prefix}.jpg")
        plt.savefig(image_path,
                    bbox_inches="tight",
                    pad_inches=0,
                    transparent=True,
                    orientation='landscape')

        # 缩小图片并保存
        resize_image(image_path, 2.58065, 0.34688)

        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return {
                "success": True,
                "data": encoded_string.decode('utf-8')
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# 定义缩小图片的函数
def resize_image(image_path, width_ratio, height_ratio):
    with Image.open(image_path) as image:
        resized_image = image.resize((int(image.size[0] * width_ratio), int(image.size[1] * height_ratio)))
        resized_image.save(image_path)
