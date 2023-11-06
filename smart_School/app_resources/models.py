from datetime import datetime
from django.utils import timezone
import pytz
from django.db import models
from dashboard.models import *


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
    return f'faces/{instance.id_national}.jpg'


class ImagesPerson(models.Model):
    image=models.ImageField(upload_to='persons\\images', blank=True, null=True)

class Persons(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    type_register = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="uploads", null=True, blank=True)
    front_national_img = models.ImageField(
        upload_to="uploads", null=True, blank=True)
    back_national_img = models.ImageField(
        upload_to="uploads", null=True, blank=True)
    id_national = models.CharField(max_length=300, null=True, blank=True)
    job_title = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=100, default='unknown')
    religion = models.CharField(max_length=100, default='مسلم')
    status_person = models.CharField(max_length=100, default='اعزب')
    created_at = models.DateTimeField(default= timezone.now())
    allowed_cameras = models.ManyToManyField(Cameras, blank=True)
    info = models.ForeignKey(
        'Information', on_delete=models.CASCADE, null=True)
    images = models.ManyToManyField(ImagesPerson,blank=True, null=True)

    def __str__(self):
        return self.name



class PersonsDetect(models.Model):
    detected_at = models.DateTimeField()
    outed_at = models.DateTimeField(null=True, blank=True)
    camera_id = models.ForeignKey(Cameras, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Persons, on_delete=models.CASCADE)
    spend_time = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.detected_at:
            self.detected_at = datetime.now().replace(second=0, microsecond=0)
        if self.camera_id.camera_type == 'outdoor':
            self.outed_at = datetime.now().replace(second=0, microsecond=0)
            indoor_detection = PersonsDetect.objects.filter(person_id=self.person_id,
                                                            camera_id__camera_type='indoor').last()
            if indoor_detection:
                time_in = indoor_detection.detected_at
                current_time = datetime.now().replace(second=0, microsecond=0, tzinfo=pytz.UTC)
                time_in = time_in.replace(tzinfo=pytz.UTC)
                self.spend_time = str(current_time - time_in)
            else:
                self.spend_time = None
        super().save(*args, **kwargs)


class Information(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)
    # employee = models.ForeignKey("Employee", on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE, null=True)
    other = models.ForeignKey(Other, on_delete=models.CASCADE, null=True)
    visior_type = models.ForeignKey(
        VisiTortype, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    empolyee=models.ForeignKey(Persons,on_delete=models.CASCADE, null=True)
