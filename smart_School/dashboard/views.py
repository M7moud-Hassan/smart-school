from datetime import date, datetime
from django.core.files.base import ContentFile
from django.shortcuts import render
import requests
from app_resources.forms import PersonsForm
from dashboard.form import FilterForm, SearchIDForm
from app_resources.models import Cameras, Information, Persons
from django.contrib.auth.decorators import login_required

import face_recognition,os
from django.conf import settings
import numpy as np

def dashboard(request):
    current_visitor=0
    avg_visitor=0
    women_count=0
    men_count=0
    months_counts= [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
    persons=[]
    form=FilterForm()  
    if request.method=='POST':
        date_range=request.POST.get('date_rang')
        department=request.POST.get('department')
        type=request.POST.get('type')
        typeVisitor=request.POST.get('typeVisitor')
        reason=request.POST.get('reason')
        other=request.POST.get('other')
        start_date, end_date = map(lambda x: datetime.strptime(x.strip(), '%m/%d/%Y'), date_range.split('-'))
        persons=Persons.objects.filter(created_at__range=(start_date, end_date),)
    else:
        form=FilterForm()  
    return render(request,'dashboard/dashboard.html',context={'sub_title':'Dashboard','form':form,
                                                              'current_visitor':current_visitor,
                                                              'avg_visitor':avg_visitor,
                                                              'women_count':women_count,
                                                              'men_count':men_count,'months_counts':months_counts,
                                                              'persons':persons})
def search_id(request):
    if request.method=='POST':
        form=SearchIDForm(request.POST,request.FILES)
        if form.is_valid():
            if form.cleaned_data['frontImage']:
                pass
            if form.cleaned_data['National_id']:
                
                pass
    else:
        form=SearchIDForm()
    return render(request,'dashboard/search_id.html',context={'form':form})

def face_id(request):
    
    form=SearchIDForm(request.POST,request.FILES)
    if form.is_valid():
            if form.cleaned_data['frontImage']:
                #try:
                        if request.method == 'POST':
                            print(settings.KNOW_FACE_NAMES)
                            file = request.FILES.get('frontImage', False) #request.FILES['front']
                            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                            print(file)
                            filename_front = file.name
                            #file.save(os.path.join('uploads',filename))
                            #filename=photos.save(form.photo.data)
                            with open(os.path.join('media','uploads',filename_front), 'wb+') as destination:
                                for chunk in file.chunks():
                                    destination.write(chunk)
                            source_front =  os.path.join('media', 'uploads', filename_front)

                            # Load an image with an unknown face
                            unknown_image = face_recognition.load_image_file(source_front)

                            # Find all the faces and face encodings in the unknown image
                            face_locations = face_recognition.face_locations(unknown_image)
                            face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
                            name = []
                            # Loop through each face found in the unknown image
                            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                                # See if the face is a match for the known face(s)
                                matches = face_recognition.compare_faces(settings.KNOW_FACE_ENCODINGS, face_encoding)

                                

                                # Or instead, use the known face with the smallest distance to the new face
                                face_distances = face_recognition.face_distance(settings.KNOW_FACE_ENCODINGS, face_encoding)
                                best_match_index = np.argmin(face_distances)
                                if matches[best_match_index]:
                                    name.append(settings.KNOW_FACE_NAMES[best_match_index])
                            
                            if len(name) >0 :
                                print(name)
                                
                            else:
                                 print("Unkonw")
                                
                #except Exception as e:
                #        return Response({'error': str(e)}) 

    return render(request,'dashboard/face_id.html',context={'form':form})