# Generated by Django 2.1.8 on 2019-04-28 13:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('upload', '0004_auto_20190416_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoprofile',
            name='is_loop',
            field=models.BooleanField(blank=True, default=False, verbose_name='ループさせる'),
        ),
        migrations.AlterField(
            model_name='videoprofile',
            name='allows_anonymous_comment',
            field=models.BooleanField(blank=True, default=True, verbose_name='匿名コメントを許可'),
        ),
    ]