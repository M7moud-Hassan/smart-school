# Generated by Django 4.2.5 on 2023-11-22 10:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0006_alter_cameras_created_at_alter_persons_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameras',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 22, 12, 59, 41, 596826)),
        ),
        migrations.AlterField(
            model_name='persons',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 22, 10, 59, 41, 596826, tzinfo=datetime.timezone.utc)),
        ),
    ]
