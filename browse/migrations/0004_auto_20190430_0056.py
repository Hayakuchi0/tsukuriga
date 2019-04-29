# Generated by Django 2.1.8 on 2019-04-29 15:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('browse', '0003_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='number',
            field=models.PositiveSmallIntegerField(unique=True, verbose_name='番号'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='channel',
            name='description',
            field=models.TextField(verbose_name='説明'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='title',
            field=models.CharField(max_length=50, verbose_name='タイトル'),
        ),
    ]
