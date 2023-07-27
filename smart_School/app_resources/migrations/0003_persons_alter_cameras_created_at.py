# Generated by Django 4.2.3 on 2023-07-24 09:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0002_cameras_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('gender', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('image', models.ImageField(upload_to='', verbose_name='persons/')),
            ],
        ),
        migrations.AlterField(
            model_name='cameras',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 24, 12, 48, 57, 696651)),
        ),
    ]