# Generated by Django 4.1.6 on 2023-08-27 22:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0002_alter_cameras_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameras',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 28, 1, 3, 10, 970707)),
        ),
        migrations.AlterField(
            model_name='personsdetect',
            name='outed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
