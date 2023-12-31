"""
URL configuration for smart_School project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
   path('',index,name="index"),
   path('result_cameras/<int:pk>/',result_cameras,name="result_cameras"),
   path('show/<int:pk>/',show_table,name="show_table"),
   path('filter_camera/<str:filter_date>/<int:camera_id>',filter_camera,name="filter_camera"),
   path('logout/',logout_view,name="logout")
]
