# Generated by Django 4.2.5 on 2023-12-13 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0007_reasons_num_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='token_access',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='url_whatsapp',
            field=models.URLField(default='https://graph.facebook.com/v17.0/119791417748534/messages'),
        ),
    ]