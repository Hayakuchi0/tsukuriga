# Generated by Django 2.1.7 on 2019-03-13 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('notify', '0002_notification_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='target_content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='target_object_id',
            field=models.IntegerField(),
            preserve_default=False,
        ),
    ]
