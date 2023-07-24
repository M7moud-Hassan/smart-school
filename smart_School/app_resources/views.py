import io

from django.views.decorators import gzip

from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from .models import Cameras, Persons
from .forms import CamerasForm, PersonsForm
from .utils import *
import cv2


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
            "form": form,
            "add_or_update": "add"
        })


def all_cameras(request):
    cameras = Cameras.objects.all()
    return render(request, 'camera/cameras.html', context={"cameras": cameras,
                                                           "title": "Camera",
                                                           "sub_title": "Cameras",
                                                           })


def edit_camera(request, id):
    camera = Cameras.objects.filter(id=id).first()
    if request.method == 'POST':
        form = CamerasForm(request.POST, instance=camera)
        if form.is_valid():
            form.save()
            return redirect('/cameras/cameras')
    else:
        if camera:
            form = CamerasForm(instance=camera)
            return render(request, 'camera/add_camera.html', context={
                "title": "Camera",
                "form": form,
                "add_or_update": "update"
            })
        else:
            return redirect('/cameras/cameras')


def delete_camera(request, id):
    camera = Cameras.objects.filter(id=id).first()
    if camera:
        camera.delete()
        return redirect('/cameras/cameras/')
    else:
        return redirect('/cameras/cameras/')


def add_person(request):
    cameras = Cameras.objects.all()
    if request.method == 'POST':
        form = PersonsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/persons/persons/')
        else:
            return render(request, 'persons/add_persons.html', context={'form': form,
                                                                        "title": "Persons",
                                                                        "sub_title": "Add Person",
                                                                        "update_or_add": "add",
                                                                        "cameras": cameras
                                                                        })
    else:
        form = PersonsForm()
        return render(request, 'persons/add_persons.html', context={'form': form,
                                                                    "title": "Persons",
                                                                    "sub_title": "Add Person",
                                                                    "update_or_add": "add",
                                                                    "cameras": cameras
                                                                    })


def edit_person(request, id):
    person = Persons.objects.filter(id=id).first()
    if request.method == 'POST':
        form = PersonsForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('/persons/persons/')
    else:
        if person:
            form = PersonsForm(instance=person)
            return render(request, 'persons/add_persons.html', context={
                "title": "Add Person",
                "form": form,
                "update_or_add": "update",
                "cameras":Cameras.objects.all()
            })
        else:
            return redirect('/persons/persons')


def persons(request):
    persons_lis = Persons.objects.all()
    return render(request, 'persons/persons.html', context={"persons": persons_lis, "title": "Persons",
                                                            "sub_title": "Persons", })


@gzip.gzip_page
@require_GET
def video_feed(request, camera_id):
    cam = Cameras.objects.filter(id=camera_id).first()
    connection_string = cam.connection_string
    if connection_string == '0':
        connection_string = int(connection_string)
    camera = cv2.VideoCapture(connection_string)
    cameras.append(camera)

    # Define the video codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    def generate():
        while True:
            # Read a frame from the camera
            ret, frame = camera.read()

            if not ret:
                break

            # Write the frame to the video file
            out.write(frame)

            # result = DeepFace.analyze(frame, actions=['emotion', 'age','detection'], enforce_detection=False)

            ret, jpeg = cv2.imencode('.jpg', frame)
            data = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')


def capture_image(request):
    video = cameras[-1]

    ret, frame = video.read()
    if ret:
        ret, buffer = cv2.imencode('.jpg', frame)

        image_bytes = buffer.tobytes()

        file_object = io.BytesIO(image_bytes)

        response = FileResponse(
            file_object,
            content_type='image/jpeg',
        )
        response['Content-Disposition'] = 'attachment; filename="captured_image.jpg"'
        return response
    else:
        return HttpResponse(status=204)


def release_resources(request):
    for camera in cameras:
        camera.release()
    cv2.destroyAllWindows()
    cameras.clear()
    return HttpResponse('done')
