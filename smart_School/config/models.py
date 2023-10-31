from django.db import models
# from django.utils import timezone
from datetime import time
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
        
        # Ensure that hours are within the 0..23 range
        hours = hours % 24

        end_time = time((start_time.hour + hours) % 24, start_time.minute + minutes)
        return end_time