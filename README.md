# Introduction

This project is the award-winning work of Chinese Collegiate Computing Competition (4C 2023).

# Start

Before running the project, you need to download some necessary files.

1. Please unzip [example_audio.zip](https://drive.google.com/file/d/1gSBb5BAC2uSGQ-Wnl33MIpkEnwBL_iQJ/view?usp=sharing) in the `server/media/example-audio` folder.

2. Please download the pretrained model to any location and configure the absolute path of the model in `server/configure/model.py`. We provide 2 pretrained model:

- [val_TimmClassifier_efficientnet_b4_0_f1_score_v1](https://drive.google.com/file/d/1XmROwLfGu17UX79JPvHolgVxe10faMpi/view?usp=sharing)
- [val_TimmClassifier_efficientnet_b4_0_f1_score_v2](https://drive.google.com/file/d/1fCiaUyFsVCc84ZCfQHHHibhfhz8Iozsy/view?usp=sharing)

3. If you need to use the email registration function, please configure the email server in `server/email.py`

## server

```shell
cd server/
pip install -r ./requirements.txt
python ./manage.py makemigrations
python ./manage.py migrate
python ./manage.py runserver 8000
```

## client

```shell
npm install
npm run serve
```

# Contact

If you have any questions about this project, please contact:

```
model: dream18455215141@163.com
client: wufangiu666666@163.com
server: hdxin2002@gmail.com
```

# Citation

If this project is helpful to you, please cite it in your paper:

```bibtex
@software{Bird_Sound_Classification,
  author = {Xiang Li and Fang Wu and Haidong Xin},
  title = {{Bird_Sound_Classification}},
  url = {https://github.com/xhd0728/Bird_Sound_Classification},
  version = {1.0},
  year = {2024}
}
```