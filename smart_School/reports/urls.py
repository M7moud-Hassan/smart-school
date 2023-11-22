from django.urls import path
from .views import *
urlpatterns = [
   path('report/',report,name="report"),
   path('load_data/<str:date>/',load_data,name="load_data"),
  
]
