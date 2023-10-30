# Generated by Django 4.2.5 on 2023-10-22 15:32

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0005_alter_cameras_created_at_alter_persons_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persons',
            name='nationalID',
        ),
        migrations.AddField(
            model_name='persons',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to='images/'), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='cameras',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 18, 32, 9, 868003)),
        ),
        migrations.AlterField(
            model_name='persons',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 15, 32, 9, 868003, tzinfo=datetime.timezone.utc)),
        ),
    ]