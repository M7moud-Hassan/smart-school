from datetime import date, datetime
from django.core.files.base import ContentFile
from django.shortcuts import render
import requests
from app_resources.forms import PersonsForm
from dashboard.form import FilterForm, SearchIDForm
from app_resources.models import Cameras, Information, Persons
from django.contrib.auth.decorators import login_required


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
    form=SearchIDForm()
    return render(request,'dashboard/face_id.html',context={'form':form})