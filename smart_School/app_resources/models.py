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


class Persons(models.Model):
    name = models.CharField(max_length=300)
    gender = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    image= models.ImageField( upload_to='persons/')
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now())
