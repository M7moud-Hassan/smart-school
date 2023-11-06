import base64
from datetime import date, datetime
import json
from django.core.files.base import ContentFile
from django.shortcuts import redirect, render
import requests
from app_resources.forms import PersonsForm
from config.models import Config
from dashboard.form import FilterForm, SearchIDForm
from app_resources.models import Cameras, Information, Persons
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from django.conf import settings
import numpy as np



def search_id(request):
    if request.method == 'POST':
        form = SearchIDForm(request.POST, request.FILES)
        if form.is_valid():
            image=request.POST.get('frontImage')
            if  image:
                picture = request.POST.get('image')
                data = json.loads(image)
                picture = ContentFile(base64.b64decode(data['data']),name=data['name'])
                api_url = Config.objects.all().first().url_extract_data
                files = {'file': ('filename.jpg', picture, 'image/jpeg')}
                response = requests.post(api_url, files=files)
                response_json = json.loads(response.text)
                person = Persons.objects.filter(id_national=response_json.get('iden').replace(' ', ''))
                if person:
                   return redirect('/persons/view_person/'+str(person.first().id))
                else:
                    messages.error(request, ' الشخص غير موجود ' +response_json.get('iden').replace(' ', ''))
                    
            if form.cleaned_data['National_id']:
                person=Persons.objects.filter(id_national=form.cleaned_data['National_id'])
                if person:
                    redirect('/persons/view_person/'+person.first().id)
                else:
                    messages.error(request, ' الشخص غير موجود ' +form.cleaned_data['National_id'])
    else:
        form = SearchIDForm()
    return render(request, 'dashboard/search_id.html', context={'form': form, "cameras":Cameras.objects.all(),})


def face_id(request):
    form = SearchIDForm()
    if request.method == 'POST':
        form = SearchIDForm(request.POST, request.FILES)
        if form.is_valid():
            image=request.POST.get('frontImage')
            if image:
                data = json.loads(image)
                data_image = ContentFile(base64.b64decode(data['data']),name=data['name'])
                print(data_image)
                face_function(data_image)
            

    return render(request, 'dashboard/face_id.html', context={'form': form, "cameras":Cameras.objects.all(),})


MODEL =  "hog"  #hog "cnn"
TOLERANCE = 0.55 
def face_function(data_image):
    with open(os.path.join('media', 'uploads', data_image), 'wb+') as destination:
        for chunk in destination.chunks():
            destination.write(chunk)
    source_front = os.path.join('media', 'uploads', data_image)

            # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(source_front)

            # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    name = ""
                    # Loop through each face found in the unknown image
    for face_encoding in  face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(settings.KNOW_FACE_ENCODINGS, face_encoding,tolerance=TOLERANCE)

                        

                        # Or instead, use the known face with the smallest distance to the new face
                        face_distances = face_recognition.face_distance(settings.KNOW_FACE_ENCODINGS, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name.append(settings.KNOW_FACE_NAMES[best_match_index])
                    
                        if matches[best_match_index] :
                            print(settings.KNOW_FACE_NAMES[best_match_index])
                            if "_"in settings.KNOW_FACE_NAMES[best_match_index]:
                                name= settings.KNOW_FACE_NAMES[best_match_index].split("_")[0]
                                 #detect_person(settings.KNOW_FACE_NAMES[best_match_index].split("_")[0],camera_id)
                            else:
                                name = settings.KNOW_FACE_NAMES[best_match_index]
                                #detect_person(settings.KNOW_FACE_NAMES[best_match_index],camera_id)
                            print("////////////////////////////////////////////")
                        else:
                            #detect_unknown(frame,camera_id)
                            name ="-1"
                            print("unknow !!!!!!!!!!!!!!!!!!!!!")

        
    
    return name
