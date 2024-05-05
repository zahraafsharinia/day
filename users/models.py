from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from extensions.utils import jalali_converter
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    national_number = models.CharField(max_length=10, unique=True, verbose_name='کدملی')
    personnel_code = models.IntegerField(default=0, verbose_name='کدپرسنلی')
    branch_code = models.CharField(max_length=4, verbose_name='کد شعبه')
    organization_code = models.IntegerField(default=0, verbose_name='کد سازمان')
    organization_name = models.CharField(max_length=32, verbose_name='نام سازمان')
    sub_organization_name = models.CharField(max_length=32, verbose_name='نام زیر سازمان')
    post_code = models.IntegerField(default=0, verbose_name='کد پست')
    post_name = models.CharField(max_length=32, verbose_name='نام پست')
    post_level_code = models.IntegerField(default=0, verbose_name='کد سطح پست')
    post_level_name = models.CharField(max_length=32, verbose_name='نام سطح پست')
    status_name = models.CharField(max_length=16, verbose_name='وضعیت')
    # last_login = jDateTimeField(blank=True, null=True, verbose_name='آخرین ورود')
    # last_login_j = models.DateTimeField(default=timezone.now, verbose_name='آخرین ورود')

    objects = CustomUserManager()

    def __str__(self):
        return self.national_number

    def last_login_j(self):
        return jalali_converter(self.last_login)
