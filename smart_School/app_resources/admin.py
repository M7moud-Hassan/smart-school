from django.contrib import admin

from .models import Cameras, Persons, PersonsDetect

admin.site.register(Cameras)
admin.site.register(Persons)
admin.site.register(PersonsDetect)
