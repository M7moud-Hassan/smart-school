from django.shortcuts import render, redirect

from .models import Cameras
from .forms import CamerasForm


# Create your views here.
def add_camera(request):
    if request.method == 'POST':
        form = CamerasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/cameras/cameras/')
    else:
        form = CamerasForm()
        return render(request, 'camera/add_camera.html', context={
            "title": "Camera",
            "sub_title": "Add Camera",
            "form": form
        })


def all_cameras(request):
    cameras = Cameras.objects.all()
    return render(request, 'camera/cameras.html', context={"cameras": cameras,
                                                           "title": "Camera",
                                                           "sub_title": "Cameras",
                                                           })
