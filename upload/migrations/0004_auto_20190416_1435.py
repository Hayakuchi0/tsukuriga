# Generated by Django 2.1.8 on 2019-04-16 05:35

import django.core.files.storage
from django.db import migrations, models
import upload.models
import upload.validators


class Migration(migrations.Migration):
    dependencies = [
        ('upload', '0003_videoprofile_allows_anonymous_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedpurevideo',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(),
                                   upload_to=upload.models.temp_upload_to, validators=[
                    upload.validators.FileValidator(allowed_extensions=['mp4', 'avi', 'gif', 'mov'],
                                                    max_size=104857600), upload.validators.video_file_validator],
                                   verbose_name='動画ファイル'),
        ),
    ]