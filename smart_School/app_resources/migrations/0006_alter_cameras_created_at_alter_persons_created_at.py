# Generated by Django 4.2.5 on 2023-11-21 23:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0005_alter_cameras_created_at_alter_persons_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameras',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 22, 1, 39, 48, 657236)),
        ),
        migrations.AlterField(
            model_name='persons',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 21, 23, 39, 48, 657236, tzinfo=datetime.timezone.utc)),
        ),
    ]
