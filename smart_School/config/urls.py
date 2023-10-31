from django.urls import path
from .views import *
urlpatterns = [
    path('add_files/',add_files,name='add_files'),
    path('result_files/',result_files,name='result_files'),
    path('config/',importatnted_fileds,name='importatnted_fileds')
]