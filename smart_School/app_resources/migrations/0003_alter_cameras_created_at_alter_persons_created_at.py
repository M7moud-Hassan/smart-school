# Generated by Django 4.2.3 on 2023-08-08 12:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0002_alter_cameras_created_at_alter_persons_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameras',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 8, 15, 27, 43, 273841)),
        ),
        migrations.AlterField(
            model_name='persons',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]