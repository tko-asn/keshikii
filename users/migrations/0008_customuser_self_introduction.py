# Generated by Django 3.2 on 2021-04-27 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_customuser_favorite_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='self_introduction',
            field=models.TextField(blank=True, null=True, verbose_name='自己紹介'),
        ),
    ]
