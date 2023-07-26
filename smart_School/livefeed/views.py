from django.shortcuts import render

from app_resources.models import *


# Create your views here.
def all_cameras(request):
    camears = Cameras.objects.all()
    return render(request, 'livefeed/all.html', context={
        "title": "View Cameras",
        "sub_title": "All",
        "cameras": camears
    })


def open_camera(request, id):
    camera=Cameras.objects.filter(id=id).first()
    return render(request, 'livefeed/live_camera.html', context={
        "cameras": Cameras.objects.all(),
        "camera":camera
    })
