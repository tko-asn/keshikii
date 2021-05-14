from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.conf import settings

import uuid
import base64
import os


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('ユーザー名の登録は必須です。')
        username = self.model.normalize_username(username)
        user = self.model(
            username=username, 
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        if not extra_fields.get('is_staff'): 
           raise ValueError('スタッフ権限が認められません。')
        if not extra_fields.get('is_superuser'):
           raise ValueError('管理者権限が認められません。')
        return self._create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ユーザーモデル"""

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    username = models.CharField(
        verbose_name='ユーザー名',
        max_length=100,
        unique=True,
    )
    icon = models.ImageField(
        upload_to='user_icons/',
        verbose_name='ユーザーアイコン',
        validators=[FileExtensionValidator(['jpeg', 'jpg'])],
        default='user_icons/default_user_icon.jpeg',
        blank=True,
    )
    self_introduction = models.TextField(
        verbose_name='自己紹介',
        null=True,
        blank=True,
    )
    favorite_posts = models.ManyToManyField(
        'posts.Post',
        verbose_name='お気に入りの投稿',
        blank=True,
        related_name='users_favorite_posts',
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    registered_date = models.DateTimeField(
        verbose_name='作成日時',
        default=timezone.now,
    )
    objects = UserManager()

    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'
        db_table = 'custom_user'

    USERNAME_FIELD = 'username'

    @property
    def icon_url(self):
        if settings.DEBUG:
            try:
                with open(self.icon.path, 'rb') as f:
                    data = f.read()
                encode_data = base64.b64encode(data)
            except:
                print('error')
                return 'kdk'
        else:
            import requests
            r = requests.get(self.icon.url)
            encode_data = base64.b64encode(r.content)
        return "data:image/jpeg;base64,{}".format(encode_data.decode())

    @property
    def icon_filename(self):
        return os.path.basename(self.icon.name)

    def __str__(self):
        return self.username
        

class Following(models.Model):
    """フォローモデル"""

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    followed_by = models.ForeignKey(
        get_user_model(), 
        verbose_name='フォローユーザー',
        on_delete=models.CASCADE,
        null=True,
        related_name='followed_by',
    )
    followed_user = models.ForeignKey(
        get_user_model(), 
        verbose_name='入力用フォロー対象',
        on_delete=models.CASCADE, 
        null=True,
        related_name='followed_user',
    )
    
    class Meta:
        verbose_name = 'フォロー'
        verbose_name_plural = 'フォロー'
        db_table = 'following'

    def __str__(self):
        return '{} followed by {}'.format(
            self.followed_user, self.followed_by.username
        )