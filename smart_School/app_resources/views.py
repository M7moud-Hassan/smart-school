import base64
from django.core.files.base import ContentFile
# import pybase64
import io
import json
from datetime import datetime
import cv2
from django.db.models import Q
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from .models import Cameras, ImagesPerson, Persons, PersonsDetect
from .forms import CamerasForm, InformationsForm, PersonsForm
from .utils import cameras
import requests
from livefeed.utils import image_of_person, image_update_person
import imutils
from imutils.video import VideoStream
import os
import pickle
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

@login_required
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

@login_required
def all_cameras(request):
    camera_all = Cameras.objects.all()
    return render(request, 'camera/cameras.html', context={"cameras": camera_all,
                                                           "title": "Camera",
                                                           "sub_title": "Cameras",
                                                           })

@login_required
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

@login_required
def delete_camera(request, id):
    camera = Cameras.objects.filter(id=id).first()
    if camera:
        camera.delete()
        return redirect('/cameras/cameras/')
    else:
        return redirect('/cameras/cameras/')


def add_padding(base64_string):
    while len(base64_string) % 4 != 0:
        base64_string += '='
    return base64_string

@login_required
def add_person(request):
    cameras_list = Cameras.objects.all()
    if request.method == 'POST':
        form = PersonsForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['type_register']=='Visitor':
                inforForm=InformationsForm(request.POST)
                if inforForm.is_valid():
                    person_instance = form.save(commit=False)
                    info_intsance=inforForm.save()
                    person_instance.info=info_intsance
                    # person_instance.images=image_list
                    person_instance.save()
                    person_instance = form.save()
                    base64_images = request.POST.getlist('images')
                    for base64_image in base64_images:
                        try:
                            data = json.loads(base64_image)
                            data_image = ContentFile(base64.b64decode(data['data']),name=data['name'])
                            im=ImagesPerson.objects.create(image=data_image)
                            person_instance.images.add(im)
                        except:
                            pass
                    person_instance.save()
            else:
                    person_instance = form.save()
                    base64_images = request.POST.getlist('images')
                    for base64_image in base64_images:
                        try:
                            data = json.loads(base64_image)
                            data_image = ContentFile(base64.b64decode(data['data']),name=data['name'])
                            im=ImagesPerson.objects.create(image=data_image)
                            person_instance.images.add(im)
                        except:
                            pass
                    person_instance.save()
            image_of_person(person_instance)
            return redirect('/persons/persons/')
        else:
            return render(request, 'persons/add_persons.html', context={'form': form,
                                                                        "title": "Persons",
                                                                        "sub_title": "Add Person",
                                                                        "update_or_add": "add",
                                                                        "cameras": cameras_list
                                                                        })
    else:
        form = PersonsForm()
        inforForm=InformationsForm()
        return render(request, 'persons/add_persons.html', context={'form': form,
                                                                    "title": "Persons",
                                                                    "sub_title": "Add Person",
                                                                    "update_or_add": "add",
                                                                    "cameras": cameras_list,
                                                                    'info_form':inforForm
                                                                    })

@login_required
def edit_person(request, id):
    person = Persons.objects.filter(id=id).first()
    if request.method == 'POST':
        form = PersonsForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            person_instance = form.save()
            
            # image_update_person(person_instance)
            return redirect('/persons/persons/')
    else:
        if person:

            form = PersonsForm(instance=person,
                               initial={'image': '', 'front_national_img': '',
                                        'date_of_birth': person.date_of_birth.strftime(
                                            '%m/%d/%Y') if person.date_of_birth else ''})
            form.fields['image'].widget.attrs['data-default-file'] = "http://127.0.0.1:8000/" + person.image.url
            form.fields['front_national_img'].widget.attrs[
                'data-default-file'] = "http://127.0.0.1:8000/" + person.front_national_img.url
            return render(request, 'persons/add_persons.html', context={
                "title": "Add Person",
                "form": form,
                "update_or_add": "update",
                "cameras": Cameras.objects.all(),
                "image": person.image,
                'ids_camera': person.allowed_cameras.all().values_list('id', flat=True)
            })
        else:
            return redirect('/persons/persons')

@login_required
def persons(request):
    persons_list = Persons.objects.filter(~Q(status='unknown'))
    return render(request, 'persons/persons.html', context={"persons": persons_list, "title": "Persons",
                                                            "sub_title": "Persons", })


"""def delete_person(request, id):
    
    person = Persons.objects.filter(id=id).first()
    person.delete()
    return redirect('/persons/persons')"""
@login_required
def delete_person(request, id):
    person = Persons.objects.filter(id=id).first()

    if person:
        # Delete the person's representation from the list
        #delete_representation(person)

        # Delete the person from the database
        person.delete()

    return redirect('/persons/persons')
@login_required
def delete_representation(person):
    pickle_file_path = os.path.join(settings.MEDIA_ROOT, 'representations.pkl')

    if os.path.exists(pickle_file_path):
        with open(pickle_file_path, "rb") as f:
            representations = pickle.load(f)
            representations = [rep for rep in representations if rep[2] != person.id]  # Remove person's representation
        with open(pickle_file_path, "wb") as f:
            pickle.dump(representations, f)
            print(len(representations))

@login_required
def view_person(request, id):
    person = Persons.objects.filter(id=id).first()
    report = False
    if request.method == 'POST':
        report = True
        date_range = request.POST.get('date_renge')
        start_date_str, end_date_str = date_range.split(' - ')

        start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date()
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()

        detections = PersonsDetect.objects.filter(person_id=person, detected_at__range=(start_date, end_date))
    else:
        detections = PersonsDetect.objects.filter(person_id=person)
    return render(request, 'persons/profile_person.html',
                  context={"person": person, "report": report, "title": "Persons", 'detections': detections})

@login_required
def capture_image(request):
    video = cameras[-1]['camera']
    frame = video.read()
    if frame is not None:
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

@login_required
def release_resources(request):
    try:
        # for camera in cameras:
        #     print(camera['camera'])
        #     camera['camera'].stream.stream.release()
        # cameras.clear()
        pass
    except:
        pass
    return HttpResponse('done')

@login_required
def release_camera(request, id):
    try:
        for camera in cameras:
            if camera['id'] == id:
                camera['camera'].stream.stream.release()
    except:
        pass
    return HttpResponse('done')

@login_required
@require_GET
def video_feed(request, camera_id):
    cam = Cameras.objects.filter(id=camera_id).first()
    if not cam:
        return HttpResponse("Camera not found", status=404)
    connection_string = cam.connection_string
    if connection_string == '0':
        connection_string = 0

    camera = VideoStream(connection_string)
    camera.start()

    cameras.append({"id": cam.id, "camera": camera})

    def stream_generator():
        try:
            while True:
                frame = camera.read()
                if frame is None:
                    continue
                frame = imutils.resize(frame, width=1000, height=1000)
                _, jpeg = cv2.imencode('.jpg', frame)
                data = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
        except GeneratorExit:
            camera.stop()

    return StreamingHttpResponse(stream_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

@login_required
def get_details_from_national_img(request):
    if request.method == 'POST':
        picture = request.FILES.get('image')
        api_url = 'http://24.144.84.0:9090/api/'
        files = {'file': ('filename.jpg', picture.read(), 'image/jpeg')}
        response = requests.post(api_url, files=files)
        response_json = json.loads(response.text)
        image_url = "http://24.144.84.0:9090/"+response_json.get('face_photo')[1:]
        headers = {'Origin': '*'}

        response2 = requests.get(image_url, headers=headers)

        response_data = {
            "response": response.text,
            "image": base64.b64encode(response2.content).decode('utf-8')
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
@login_required
def get_details_from_back_national_img(request):
    if request.method == 'POST':
        picture = request.FILES.get('image')
        api_url = 'http://24.144.84.0:9090/api_back/'
        files = {'file': ('filename.jpg', picture.read(), 'image/jpeg')}
        response = requests.post(api_url, files=files)
        response_json = json.loads(response.text)
        print(response_json)
        response_data = {
            "response": response.text,
           
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
