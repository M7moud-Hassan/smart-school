# Generated by Django 4.2.5 on 2023-12-13 15:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0014_alter_cameras_created_at_alter_persons_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameras',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 15, 27, 31, 717770, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='persons',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 15, 27, 31, 718771, tzinfo=datetime.timezone.utc)),
        ),
    ]
