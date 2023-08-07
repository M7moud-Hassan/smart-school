from datetime import datetime

from django.db import models


class Cameras(models.Model):
    """Data model for cameras."""
    name = models.CharField(max_length=300)
    camera_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)
    connection_string = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name


def get_upload_path(instance, filename):
    return f'persons/{instance.status}/{filename}'


class Persons(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    status = models.CharField(max_length=100, default='unknown')
    created_at = models.DateTimeField(default=datetime.now())
    allowed_cameras = models.ManyToManyField(Cameras, blank=True)


class PersonsDetect(models.Model):
    detected_at = models.DateTimeField(default=datetime.now())
    camera_id = models.ForeignKey(Cameras, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Persons, on_delete=models.CASCADE)
