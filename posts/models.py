from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.conf import settings

import uuid
import os
import base64


class Category(models.Model):
    """投稿のカテゴリーモデル"""

    name = models.CharField(
        verbose_name='カテゴリー名', 
        max_length=50,
        null=True,
    )

    class Meta:
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー'
        db_table = 'category'

    def __str__(self):
        return self.name

        
class Post(models.Model):
    """投稿モデル"""

    STATUS_CHOICES = (
        ('private', '非公開'),
        ('public', '公開'),
    )
    id = models.UUIDField(
        primary_key=True, 
        editable=False, 
        default=uuid.uuid4
    )
    title = models.CharField(
        verbose_name='タイトル', 
        max_length=50,
        null=True,
    )
    text = models.TextField(
        verbose_name='説明',
        blank=True,
        null=True,
    )
    posted_date = models.DateTimeField(
        verbose_name='投稿日時', 
        default=timezone.now
    )
    status = models.CharField(
        verbose_name='公開設定',
        choices=STATUS_CHOICES,
        default='public',
        max_length=7,
    )
    picture = models.ImageField(
        upload_to='posts/',
        verbose_name='画像',
        validators=[FileExtensionValidator(['jpeg', 'jpg'])],
        null=True,
    )
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='投稿者', 
        on_delete=models.CASCADE, 
        null=True
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='カテゴリー',
        blank=True,
    )
    zip_code = models.CharField(
        verbose_name='撮影場所郵便番号',
        max_length=20,
        null=True,
        blank=True,
    )
    prefecture = models.CharField(
        verbose_name='撮影した都道府県',
        max_length=10,
        null=True,
        blank=True,
    )
    location = models.CharField(
        verbose_name='撮影住所',
        max_length=100,
        null=True,
        blank=True,
    )

    @property
    def picture_url(self):
        if settings.DEBUG:
            with open(self.picture.path, 'rb') as f:
                data = f.read()
            encode_data = base64.b64encode(data)
        else:
            import requests
            r = requests.get(self.picture.url)
            encode_data = base64.b64encode(r.content)
        return "data:image/jpeg;base64,{}".format(encode_data.decode())
    
    @property
    def picture_filename(self):
        return os.path.basename(self.picture.name)

    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = '投稿リスト'
        db_table = 'post'

    def __str__(self):
        return self.title