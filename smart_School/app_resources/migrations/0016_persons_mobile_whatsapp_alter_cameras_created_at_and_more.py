# Generated by Django 4.2.5 on 2023-12-13 16:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0015_alter_cameras_created_at_alter_persons_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='persons',
            name='mobile_whatsapp',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cameras',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 16, 14, 22, 18584, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='persons',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 16, 14, 22, 19587, tzinfo=datetime.timezone.utc)),
        ),
    ]
