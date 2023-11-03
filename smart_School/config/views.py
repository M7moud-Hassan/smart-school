import copy
import csv
from datetime import datetime
import io
import sqlite3
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render

from app_resources.models import Cameras, Persons
from config.forms import ConfigForm
from config.models import Config
content_message=[]
def result_files(request):
     temp=copy.deepcopy(content_message)
     content_message.clear()
     return JsonResponse({'strings': temp})

def add_files(request):
    code=0
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            content_message.append('Start uploading file ' + uploaded_file.name)
            if not uploaded_file.name.endswith('.csv'):
                content_message.append('Only CSV files are allowed.')
                return HttpResponseBadRequest('Only CSV files are allowed.')
            else:
                try:
                    # id,national_id,firstname,lastname,address_1,birthday,address_2,job,gender,religion,status,id_front,id_back,branch_id,face_id_id,created_at
                    # Read and process the CSV file
                    data = 0
                    with uploaded_file:
                        text_file = io.TextIOWrapper(uploaded_file, encoding='utf-8')
                        reader = csv.reader(text_file)
                        header = next(reader)
                       
                        content_message.append(header)
                        if header==['id','national_id','firstname','lastname','address_1','birthday','address_2','job','gender','religion','status','id_front','id_back','branch_id','face_id_id','created_at']:
                            for row in reader:
                                try:
                                    date_birth=datetime.strptime(row[5], "%d-%m-%Y")
                                except:
                                    date_birth=None
                                data=data+1
                                Persons.objects.create(name=row[2]+' '+row[3],gender='Male' if row[8]=='ذكر' else 'Female',
                                                       type_register='Employee',date_of_birth=date_birth,image='/faces/'+row[1]+'.jpg',
                                                       front_national_img=row[12].replace('/media',''),back_national_img=row[13].replace('/media',''),id_national=row[1],
                                                       job_title=row[7],address=row[4]+' '+row[6],status='whitelist',created_at=row[15],
                                                       religion=row[9],status_person=row[10])
                                content_message.append('read row '+str(data))
                        else:
                            code=1
                            content_message.append('this file not contain required column')

                    content_message.append(f'Successfully processed {data} rows from {uploaded_file.name}')
                except FileNotFoundError:
                    code=1
                    content_message.append("The CSV file was not found.")
                except Exception as e:
                    code=1
                    content_message.append(f"An error occurred: {str(e)}")
            content_message.append('Exit '+str(code))

    return render(request, 'config/add_files.html',context={ "cameras":Cameras.objects.all(),})

def importatnted_fileds(request):
    instance=Config.objects.all().first()
    if instance:
        form=ConfigForm(instance=instance)
    else:
        form=ConfigForm()
    if request.method=='POST':
        if instance:
            form=ConfigForm(instance=instance,data=request.POST)
        else:
            form=ConfigForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'config/important_filed.html',context={'cameras':Cameras.objects.all(),'form':form})