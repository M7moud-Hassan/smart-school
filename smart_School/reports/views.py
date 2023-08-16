from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect

from app_resources.models import PersonsDetect, Cameras
from livefeed.utils import search_by_image_unknown_filter, search_by_image_black_filter, search_by_image_all_filter, \
    search_by_image_known_filter, search_by_image_white_filter


def reports_all_people(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        if isinstance(uploaded_file, InMemoryUploadedFile):
            persons = search_by_image_all_filter(uploaded_file)
            print(persons)
            return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                           'sub_title': 'known persons',
                                                                           'cameras': Cameras.objects.all()})
        else:
            return redirect('/reports/reports_known_people/')
    else:
        persons = PersonsDetect.objects.all()
        return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                    'sub_title': 'all reports',
                                                                'cameras': Cameras.objects.all()})


def reports_known_people(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        if isinstance(uploaded_file, InMemoryUploadedFile):
            persons = search_by_image_known_filter(uploaded_file)
            return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                           'sub_title': 'known persons',
                                                                           'cameras': Cameras.objects.all()})
        else:
            return redirect('/reports/reports_known_people/')
    else:
        persons = PersonsDetect.objects.filter(person_id__status__in=['whitelist', 'blacklist'])
        return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                'sub_title': 'known persons',
                                                                'cameras': Cameras.objects.all()})


def reports_unknown_people(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        if isinstance(uploaded_file, InMemoryUploadedFile):
            persons = search_by_image_unknown_filter(uploaded_file)
            return render(request, 'reports/unknown_person.html', context={'persons': persons, 'title': 'reports',
                                                                           'sub_title': 'unknown persons',
                                                                           'cameras': Cameras.objects.all()})
        else:
            return redirect('/reports/reports_unknown_people/')
    else:
        persons = PersonsDetect.objects.filter(person_id__status='unknown')
        return render(request, 'reports/unknown_person.html', context={'persons': persons, 'title': 'reports',
                                                                       'sub_title': 'unknown persons',
                                                                   'cameras': Cameras.objects.all()})


def reports_white_people(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        if isinstance(uploaded_file, InMemoryUploadedFile):
            persons = search_by_image_white_filter(uploaded_file)
            return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                           'sub_title': 'white persons',
                                                                           'cameras': Cameras.objects.all()})
        else:
            return redirect('/reports/reports_white_people/')
    else:
        persons = PersonsDetect.objects.filter(person_id__status='whitelist')
        return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                'sub_title': 'white persons',
                                                                'cameras': Cameras.objects.all()})


def reports_black_people(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        if isinstance(uploaded_file, InMemoryUploadedFile):
            persons = search_by_image_black_filter(uploaded_file)
            return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                           'sub_title': 'black persons',
                                                                           'cameras': Cameras.objects.all()})
        else:
            return redirect('/reports/reports_black_people/')
    else:
        persons = PersonsDetect.objects.filter(person_id__status='blacklist')
        return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                    'sub_title': 'black persons',
                                                                'cameras': Cameras.objects.all()})

