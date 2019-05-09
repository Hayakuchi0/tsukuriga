# Generated by Django 2.1.8 on 2019-05-09 11:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('browse', '0011_auto_20190430_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='type',
            field=models.CharField(choices=[('popular', '人気順'), ('favorites', 'お気に入り順')], default='popular',
                                   max_length=20, verbose_name='集計タイプ'),
        ),
    ]
