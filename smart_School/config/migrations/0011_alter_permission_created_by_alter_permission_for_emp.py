# Generated by Django 4.2.5 on 2023-12-21 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0019_alter_cameras_created_at_alter_persons_created_at'),
        ('config', '0010_permission_reason_remove_permission_for_emp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_permissions', to='app_resources.persons'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='for_emp',
            field=models.ManyToManyField(blank=True, to='app_resources.persons'),
        ),
    ]
