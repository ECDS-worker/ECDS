from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

# Create your models here.


class UserProfile(AbstractUser):
    """
    用户表，新型字段
    """
    GEBDER_CHOICES = (
        ("male", "男"),
        ("female", "女")
    )
    name = models.CharField(max_length=32, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=8, choices=GEBDER_CHOICES, default="female", verbose_name="性别")

    class Meta:
        db_table = 'User'
        verbose_name = "用户"
        # 使表名在admin中显示特定的名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    @classmethod
    def create(cls, password, last_login, is_superuser, username, date_joined):
        return cls(password=password, last_login=last_login, is_superuser=is_superuser, username=username,
                   date_joined=date_joined)


class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(default='姓名', max_length=15, null=True, blank=True, help_text='姓名')
    age = models.IntegerField(default=1, help_text='年龄')
    gender = models.BooleanField(default=True, max_length=18, help_text='性别')
    phone = models.CharField(default='', max_length=16, blank=True, null=True, help_text="手机号码")
    email = models.EmailField(default='', blank=True, null=True, help_text='邮箱')
    address = models.CharField(default='', max_length=256, blank=True, null=True, help_text="地址")
    birthday = models.DateField(default=date(2018, 1, 1), null=True, help_text="出生日期")
    qq = models.CharField(default='', max_length=16, blank=True, null=True, help_text='qq')
    wechat = models.CharField(default='', max_length=16, blank=True, null=True, help_text='微信')
    job = models.CharField(default='', max_length=64, blank=True, null=True, help_text='工作')
    salary = models.CharField(default='', max_length=32, blank=True, null=True, help_text='薪水')

    class Meta:
        db_table = 'userinfo'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, user):
        return cls(user=user)


class Custormer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(default='名称', max_length=20, help_text='客户名称')
    email = models.CharField(default='', max_length=30, null=True, blank=True, help_text='邮箱')
    company = models.CharField(default='', max_length=40, null=True, help_text='公司名称')
    address = models.CharField(default='', max_length=50, null=True, help_text='地址')
    phone = models.CharField(default='', max_length=16, blank=True, null=True, help_text='手机号')
    mobile = models.CharField(default='', max_length=20, blank=True, null=True, help_text='固定电话')
    qq = models.CharField(default='', max_length=20, blank=True, null=True, help_text='qq')
    wechat = models.CharField(default='', max_length=20, blank=True, null=True, help_text='微信号')
    web = models.CharField(default='', max_length=50, blank=True, null=True, help_text='网站')
    industry = models.CharField(default='', max_length=50, blank=True, null=True, help_text='行业')
    description = models.TextField(default='', null=True, blank=True, help_text='公司简介')

    class Meta:
        db_table = 'Custormer'
        verbose_name = '客户信息表'
        verbose_name_plural = verbose_name

    @classmethod
    def create(cls, user, **kwargs):
        return cls(username=user, **kwargs)


class UserForm(models.Model):
    username = models.CharField(max_length=16, null=False, help_text='用户名')
    fileurl = models.CharField(max_length=512, null=False, help_text='存储路径')

    class Meta:
        db_table = 'UserForm'
        verbose_name = '上传信息表'
        verbose_name_plural = verbose_name
