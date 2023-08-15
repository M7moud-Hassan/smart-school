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
from django.urls import path,include
from django.conf.urls.static import static

from smart_School import  settings
from home import  urls
from app_resources.urls import *
from livefeed import urls as livefeed_urls
from reports import urls as reporst_urls
from test_cam import  urls as urls_cam

urlpatterns = [
    path('',include(urls)),
    path('cameras/',include(url_cameras)),
    path('persons/',include(url_persons)),
    path('admin/',admin.site.urls),
    path('livefeed/',include(livefeed_urls)),
    path('reports/',include(reporst_urls)),
    path('cam',include(urls_cam))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
