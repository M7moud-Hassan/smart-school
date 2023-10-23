# Generated by Django 4.2.5 on 2023-10-23 14:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0007_alter_cameras_created_at_alter_persons_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagesPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='persons\\images')),
            ],
        ),
        migrations.AlterField(
            model_name='cameras',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 23, 17, 6, 39, 625257)),
        ),
        migrations.AlterField(
            model_name='persons',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 23, 14, 6, 39, 625257, tzinfo=datetime.timezone.utc)),
        ),
        migrations.RemoveField(
            model_name='persons',
            name='images',
        ),
        migrations.AddField(
            model_name='persons',
            name='images',
            field=models.ManyToManyField(blank=True, null=True, to='app_resources.imagesperson'),
        ),
    ]
