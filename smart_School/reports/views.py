from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta, datetime
from app_resources.models import PersonsDetect, Cameras
# from livefeed.utils import search_by_image_unknown_filter, search_by_image_black_filter, search_by_image_all_filter, \
#     search_by_image_known_filter, search_by_image_white_filter
from reports.utils import filter_persons
from django.contrib.auth.decorators import login_required
@login_required
def reports_all_people(request):
    today = timezone.now().date()
    start_of_day = today
    end_of_day = today + timedelta(days=1)
    if request.method == 'POST':
        date_range = request.POST.get('date_renge')
        if date_range:
            start_date_str, end_date_str = date_range.split(' - ')
            start_of_day = datetime.strptime(start_date_str, '%m/%d/%Y').date()
            end_of_day = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        else:
            uploaded_file = request.FILES['image']
            if isinstance(uploaded_file, InMemoryUploadedFile):
                # persons_result = search_by_image_all_filter(uploaded_file)
                persons = filter_persons(persons_result)
                return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                               'sub_title': 'known persons',
                                                                               'cameras': Cameras.objects.all()})
            else:
                return redirect('/reports/reports_known_people/')

    persons_result = PersonsDetect.objects.filter(detected_at__range=(start_of_day, end_of_day))
    persons = filter_persons(persons_result)
    return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                    'sub_title': 'all reports',
                                                                'cameras': Cameras.objects.all()})

@login_required
def reports_known_people(request):
    today = timezone.now().date()
    start_of_day = today
    end_of_day = today + timedelta(days=1)
    if request.method == 'POST':
        date_range = request.POST.get('date_renge')
        if date_range:
            start_date_str, end_date_str = date_range.split(' - ')
            start_of_day = datetime.strptime(start_date_str, '%m/%d/%Y').date()
            end_of_day = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        else:
            uploaded_file = request.FILES['image']
            if isinstance(uploaded_file, InMemoryUploadedFile):
                # persons = search_by_image_known_filter(uploaded_file)
                persons = filter_persons(persons)
                return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                               'sub_title': 'known persons',
                                                                               'cameras': Cameras.objects.all()})
            else:
                return redirect('/reports/reports_known_people/')
    persons_result = PersonsDetect.objects.filter(person_id__status__in=['whitelist', 'blacklist'],detected_at__range=(start_of_day, end_of_day))
    persons=filter_persons(persons_result)
    return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                'sub_title': 'known persons',
                                                                'cameras': Cameras.objects.all()})

@login_required
def reports_unknown_people(request):
    today = timezone.now().date()
    start_of_day = today
    end_of_day = today + timedelta(days=1)
    if request.method == 'POST':
        date_range = request.POST.get('date_renge')
        if date_range:
            start_date_str, end_date_str = date_range.split(' - ')
            start_of_day = datetime.strptime(start_date_str, '%m/%d/%Y').date()
            end_of_day = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        else:
            uploaded_file = request.FILES['image']
            if isinstance(uploaded_file, InMemoryUploadedFile):
                # persons = search_by_image_unknown_filter(uploaded_file)
                return render(request, 'reports/unknown_person.html', context={'persons': persons, 'title': 'reports',
                                                                               'sub_title': 'unknown persons',
                                                                               'cameras': Cameras.objects.all()})
            else:
                return redirect('/reports/reports_unknown_people/')
    persons = PersonsDetect.objects.filter(person_id__status='unknown',detected_at__range=(start_of_day, end_of_day))
    return render(request, 'reports/unknown_person.html', context={'persons': persons, 'title': 'reports',
                                                                       'sub_title': 'unknown persons',
                                                                   'cameras': Cameras.objects.all()})

@login_required
def reports_white_people(request):
    today = timezone.now().date()
    start_of_day = today
    end_of_day = today + timedelta(days=1)
    if request.method == 'POST':
        date_range = request.POST.get('date_renge')
        if date_range:
            start_date_str, end_date_str = date_range.split(' - ')
            start_of_day = datetime.strptime(start_date_str, '%m/%d/%Y').date()
            end_of_day = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        else:
            uploaded_file = request.FILES['image']
            if isinstance(uploaded_file, InMemoryUploadedFile):
                # persons = search_by_image_white_filter(uploaded_file)
                persons = filter_persons(persons)
                return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                               'sub_title': 'white persons',
                                                                               'cameras': Cameras.objects.all()})
            else:
                return redirect('/reports/reports_white_people/')
    persons = PersonsDetect.objects.filter(person_id__status='whitelist',detected_at__range=(start_of_day, end_of_day))
    persons = filter_persons(persons)
    return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                'sub_title': 'white persons',
                                                                'cameras': Cameras.objects.all()})

@login_required
def reports_black_people(request):
    today = timezone.now().date()
    start_of_day = today
    end_of_day = today + timedelta(days=1)
    if request.method == 'POST':
        date_range = request.POST.get('date_renge')
        if date_range:
            start_date_str, end_date_str = date_range.split(' - ')
            start_of_day = datetime.strptime(start_date_str, '%m/%d/%Y').date()
            end_of_day = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        else:
            uploaded_file = request.FILES['image']
            if isinstance(uploaded_file, InMemoryUploadedFile):
                # persons = search_by_image_black_filter(uploaded_file)
                persons=filter_persons(persons)
                return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                               'sub_title': 'black persons',
                                                                               'cameras': Cameras.objects.all()})
            else:
                return redirect('/reports/reports_black_people/')
    persons = PersonsDetect.objects.filter(person_id__status='blacklist',detected_at__range=(start_of_day, end_of_day))
    persons = filter_persons(persons)
    return render(request, 'reports/all_persons.html', context={'persons': persons, 'title': 'reports',
                                                                    'sub_title': 'black persons',
                                                                'cameras': Cameras.objects.all()})

