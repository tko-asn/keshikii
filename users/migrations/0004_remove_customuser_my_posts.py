# Generated by Django 3.2 on 2021-04-08 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210407_0154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='my_posts',
        ),
    ]
