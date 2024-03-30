from django.contrib.auth.models import AbstractUser
from django.db import models


class Level(models.Model):
    name = models.CharField(max_length=31)


class User(AbstractUser):
    level = models.ForeignKey(Level, on_delete=models.PROTECT)
