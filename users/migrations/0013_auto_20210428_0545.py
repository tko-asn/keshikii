# Generated by Django 3.2 on 2021-04-27 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_following_followed_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='following',
            name='read_only_followed_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed_user', to=settings.AUTH_USER_MODEL, verbose_name='出力用フォロー対象'),
        ),
        migrations.AlterField(
            model_name='following',
            name='followed_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed_user_id', to=settings.AUTH_USER_MODEL, verbose_name='入力用フォロー対象'),
        ),
    ]
