# Generated by Django 2.1.7 on 2019-03-28 12:44

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0002_auto_20190314_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_banner_url',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_icon_url',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_banner',
            field=models.ImageField(blank=True, null=True, upload_to=account.models.profile_image_upload_to,
                                    verbose_name='プロフィール背景画像'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_icon',
            field=models.ImageField(blank=True, null=True, upload_to=account.models.profile_image_upload_to,
                                    verbose_name='プロフィール画像'),
        ),
    ]
