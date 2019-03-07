# Generated by Django 2.1.7 on 2019-03-07 03:16

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import upload.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedPureVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=upload.models.temp_upload_to, verbose_name='動画ファイル')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default=upload.models.default_video_slug, max_length=5, verbose_name='動画ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
        migrations.CreateModel(
            name='VideoData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(upload_to=upload.models.thumbnail_upload_to, verbose_name='サムネイル')),
                ('file', models.FileField(upload_to=upload.models.video_upload_to, verbose_name='動画ファイル')),
                ('fps', models.PositiveIntegerField(verbose_name='FPS')),
                ('duration', models.FloatField(verbose_name='動画時間')),
                ('video', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='upload.Video', verbose_name='動画')),
            ],
        ),
        migrations.CreateModel(
            name='VideoProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('title', models.CharField(max_length=50, verbose_name='タイトル')),
                ('description', models.TextField(max_length=200, verbose_name='動画説明')),
                ('video', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='upload.Video', verbose_name='動画')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='uploadedpurevideo',
            name='video',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pure', to='upload.Video', verbose_name='動画'),
        ),
    ]