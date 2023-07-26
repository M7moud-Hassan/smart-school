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

url_cameras = [
    path('add_camera/',add_camera,name="add_camera"),
    path('cameras/',all_cameras,name="cameras"),
    path('edit_camera/<int:id>/',edit_camera,name="edit_camera"),
    path('delete_camera/<int:id>/',delete_camera,name="delete_camera"),
    path('video/<int:camera_id>',video_feed,name="video"),
    path('release/',release_resources,name="release"),
    path('capture_image/',capture_image,name="capture_image"),
    path('release_camera/<int:id>',release_camera,name="release_camera")
]
url_persons= [
    path('persons/',persons,name="persons"),
    path('add_person/',add_person,name="add_person"),
    path('edit_person/<int:id>',edit_person,name="edit_person"),
    path('delete_person/<int:id>',delete_person,name='delete_person'),
    path('view_person/<int:id>',view_person,name="view_person")
]

