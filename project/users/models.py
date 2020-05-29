from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .choice import *


class UserManager(BaseUserManager):

    def create_user(self, user_id, password, email, name, phone, sns, location, genre, position, profile_image, **extra_fields):

        user = self.model(
            user_id = user_id,
            email = email,
            name = name,
            phone = phone,
            sns = sns,
            location = location,
            genre = genre,
            position = position,
            profile_image = profile_image,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, email=None, name=None, phone=None, sns=None, location=None, genre=None, position=None, profile_image=None):

        user = self.create_user(user_id, password, email, name, phone, sns, location, genre, position, profile_image)

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.level = 0

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    
    objects = UserManager()

    user_id = models.CharField(max_length=17, verbose_name="아이디", unique=True)
    password = models.CharField(max_length=256, verbose_name="비밀번호")
    email = models.EmailField(max_length=128, verbose_name="이메일", unique=True)
    name = models.CharField(max_length=35, verbose_name="이름(활동명)", null=True)
    phone = models.IntegerField(verbose_name="핸드폰번호", null=True, unique=True)
    sns = models.CharField(max_length=35, verbose_name="SNS아이디", null=True, unique=True)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=24, verbose_name="등급", default=2)
    location = models.CharField(choices=LOCATION_CHOICES, max_length=24, verbose_name="거주지", null=True)
    genre = models.CharField(choices=GENRE_CHOICES, max_length=24, verbose_name="분야", null=True)
    position = models.CharField(choices=POSITION_CHOICES, max_length=24, verbose_name="세부분야", null=True)
    profile_image = models.ImageField(upload_to='profile_image', verbose_name="프로필사진", null=True, blank=True)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='가입일', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "회원목록"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"