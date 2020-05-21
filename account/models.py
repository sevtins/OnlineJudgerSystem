from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    """
    用户的个人信息数据模型
    """
    iphone = models.CharField(max_length=64, verbose_name="手机号")
    info = models.TextField(verbose_name="用户个人简介")
    motto = models.CharField(max_length=128, verbose_name="用户个性签名")
    photo = models.ImageField(verbose_name="用户照片")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User表外键")
