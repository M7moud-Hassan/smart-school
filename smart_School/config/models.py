from django.db import models
# from django.utils import timezone
from datetime import time

from app_resources.models import Persons
# Create your models here.

class Config(models.Model):
    time_start_working=models.TimeField(default=time(8, 0))
    num_hour_working=models.DecimalField(max_digits=10,decimal_places=2,default=8)
    url_extract_data=models.URLField(default='http://24.144.84.0:9090/api/')
    url_image=models.URLField(default='http://24.144.84.0:9090/api/')
    url_extract_data_back=models.URLField(default='http://24.144.84.0:9090/api_back/')
    @property
    def time_end_working(self):
        start_time = self.time_start_working
        num_hours = self.num_hour_working
        hours, minutes = divmod(int(num_hours * 60), 60)
        hours = hours % 24

        end_time = time((start_time.hour + hours) % 24, start_time.minute + minutes)
        return end_time
    

class AddDuration(models.Model):
    name=models.CharField(max_length=100)
    num_hour_working=models.DecimalField(max_digits=10,decimal_places=2,default=8)
    persions=models.ManyToManyField(Persons,blank=True)
class Nabatshieh(models.Model):
    name=models.CharField(max_length=100)
    time_start_working=models.TimeField(default=time(8, 0))
    num_hour_working=models.DecimalField(max_digits=10,decimal_places=2,default=8)
    persions=models.ManyToManyField(Persons,blank=True)
    @property
    def time_end_working(self):
        start_time = self.time_start_working
        num_hours = self.num_hour_working
        hours, minutes = divmod(int(num_hours * 60), 60)
        hours = hours % 24
        end_time = time((start_time.hour + hours) % 24, start_time.minute + minutes)
        return end_time
    

when_chooses = [
        ('الدخول', 'الدخول'),
        ('الخروج', 'الخروج')
    ]
class Reasons(models.Model):
    name=models.CharField(max_length=200)
    fromm=models.TimeField(null=True,blank=True)
    too=models.TimeField(null=True,blank=True)
    persions=models.ManyToManyField(Persons,blank=True)
    num_reason=models.IntegerField()
    when=models.CharField(
        max_length=20,
        choices=when_chooses,
        default='entry'
    )

    