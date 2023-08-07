# Generated by Django 4.2.3 on 2023-08-07 19:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameras',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 7, 21, 8, 32, 698935)),
        ),
        migrations.AlterField(
            model_name='persons',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 7, 21, 8, 32, 698935)),
        ),
        migrations.AlterField(
            model_name='personsdetect',
            name='detected_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 7, 21, 8, 32, 699932)),
        ),
    ]