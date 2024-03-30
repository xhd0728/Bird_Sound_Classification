from django.db import models
from django.utils import timezone


class AudioUploadLoggingModel(models.Model):
    file_name = models.CharField(max_length=128)
    classic = models.CharField(max_length=32)
    create_time = models.DateTimeField(default=timezone.now)


class BirdInfo(models.Model):
    name_EN = models.CharField(max_length=128)
    name_CN = models.CharField(max_length=128)
    wiki_link = models.CharField(max_length=256)
    image_link = models.CharField(max_length=256)
