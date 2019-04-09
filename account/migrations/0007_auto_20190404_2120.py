# Generated by Django 2.1.7 on 2019-04-04 12:20

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0006_auto_20190404_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_banner',
            field=models.ImageField(blank=True, null=True, upload_to=account.models.profile_image_upload_to,
                                    verbose_name='プロフィール背景画像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_icon',
            field=models.ImageField(blank=True, null=True, upload_to=account.models.profile_image_upload_to,
                                    verbose_name='プロフィール画像'),
        ),
    ]