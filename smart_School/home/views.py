import copy
from django.contrib.auth import logout
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from app_resources.utils import object_data
from django.db.models import Q
from datetime import time, timedelta, datetime
from app_resources.models import Persons, PersonsDetect, Cameras
from config.models import Config
from dashboard.models import Department


# Create your views here.
@login_required
def index(request):
    cameras = Cameras.objects.all()
### tody
    now = datetime.now()
    start_time = datetime(now.year, now.month, now.day)
    time_intervals = [start_time + timedelta(hours=i) for i in range(0, 24, 2)]
    counts_day_emp = []
    counts_day_vis = []
    for i in range(len(time_intervals)):
        start_time = time_intervals[i]
        try:
            end_time = time_intervals[i + 1]
        except:
             end_time = time_intervals[11]
        count = PersonsDetect.objects.filter(
            detected_at__gte=start_time,
            detected_at__lt=end_time,
            person_id__type_register='موظف'
        ).count()
        count2 = PersonsDetect.objects.filter(
            detected_at__gte=start_time,
            detected_at__lt=end_time,
            person_id__type_register='زائر'
        ).count()
        counts_day_emp.append(count)
        counts_day_vis.append(count2)
    print(len(counts_day_vis))
### weeee
    start_of_week = now - timedelta(days=now.weekday())
    date_intervals = [start_of_week + timedelta(days=i) for i in range(7)]
    counts_week_emp = []
    counts_week_vis = []
    for i in range(len(date_intervals)):
        start_date = date_intervals[i]
        try:
            end_date = time_intervals[i + 1]
        except:
            end_date = time_intervals[7]
        
        count = PersonsDetect.objects.filter(
            detected_at__date__gte=start_date,
            detected_at__date__lt=end_date,
            person_id__type_register='موظف'
        ).count()
        count2 = PersonsDetect.objects.filter(
            detected_at__date__gte=start_date,
            detected_at__date__lt=end_date,
            person_id__type_register='زائر'
        ).count()
        counts_week_emp.append(count)
        counts_week_vis.append(count2)
## month
    start_of_month = datetime(now.year, now.month, 1)
    end_of_month = start_of_month.replace(day=28) + timedelta(days=4)
    date_intervals = [start_of_month + timedelta(days=5 * i) for i in range((end_of_month - start_of_month).days // 5 + 1)]
    counts_month_emp = []
    counts_month_vis = []
    for i in range(len(date_intervals) - 1):
        start_date = date_intervals[i]
        end_date = date_intervals[i + 1]
        count = PersonsDetect.objects.filter(
            detected_at__date__gte=start_date,
            detected_at__date__lt=end_date,
            person_id__type_register='موظف'
        ).count()
        count2 = PersonsDetect.objects.filter(
            detected_at__date__gte=start_date,
            detected_at__date__lt=end_date,
            person_id__type_register='زائر'
        ).count()
        counts_month_emp.append(count)
        counts_month_vis.append(count2)
    #this years
    start_of_year = datetime(now.year, 1, 1)
    date_intervals = [start_of_year.replace(month=i) for i in range(1, 13)]
    counts_year_emp = []
    counts_year_vis = []
    for i in range(len(date_intervals) - 1):
        start_date = date_intervals[i]
        end_date = date_intervals[i + 1]
        count = PersonsDetect.objects.filter(
            detected_at__date__gte=start_date,
            detected_at__date__lt=end_date,
            person_id__type_register='موظف'
        ).count()
        count2 = PersonsDetect.objects.filter(
            detected_at__date__gte=start_date,
            detected_at__date__lt=end_date,
            person_id__type_register='زائر'
        ).count()
        counts_year_emp.append(count)
        counts_year_vis.append(count2)

    departments=Department.objects.all()
    department_counts =[]
    total_deps=0
    for dep in departments:
        count=PersonsDetect.objects.filter(
            person_id__info__department=dep
        ).count()
        total_deps=total_deps+count
        department_counts.append(count)
    # registers = Persons.objects.filter(Q(status='whitelist') | Q(status='blacklist'))
    config=Config.objects.all().first()
    if config:
        time_exit=config.time_end_working
    else:
        time_exit=time(12,0)
    today = datetime.now().date()
    detected_at_datetime = datetime.combine(today, time_exit)
    
    activeEmpoly=PersonsDetect.objects.filter(person_id__type_register='موظف',outed_at=None,detected_at__date=today, detected_at__lt=detected_at_datetime).count()
    active_visitor=PersonsDetect.objects.filter(person_id__type_register='زائر',outed_at=None,detected_at__date=today, detected_at__gt=detected_at_datetime).count()
    all_visitor=PersonsDetect.objects.filter(outed_at=None,detected_at__date=today).count()
    active_visitor_after=PersonsDetect.objects.filter(person_id__type_register='زائر',outed_at=None,detected_at__date=today, detected_at__gt=detected_at_datetime).count()
   
    most_visitor = PersonsDetect.objects.filter(person_id__type_register='زائر')
    most_visitor = most_visitor.values('person_id','person_id__name','person_id__image','person_id__job_title')
    most_visitor = most_visitor.annotate(visits=Count('person_id'))
    most_visitor = most_visitor.order_by('-visits')[:5]

    most_visitor_after = PersonsDetect.objects.filter(person_id__type_register='زائر',detected_at__time__gt=config.time_end_working)
    most_visitor_after = most_visitor_after.values('person_id','person_id__name','person_id__image','person_id__job_title')
    most_visitor_after = most_visitor_after.annotate(visits=Count('person_id'))
    most_visitor_after = most_visitor_after.order_by('-visits')[:5]
    
    most_empolyee = PersonsDetect.objects.filter(person_id__type_register='موظف')
    most_empolyee = most_empolyee.values('person_id','person_id__name','person_id__image','person_id__job_title')
    most_empolyee = most_empolyee.annotate(visits=Count('person_id'))
    most_empolyee = most_empolyee.order_by('-visits')[:5]

    ####
    most_visitor_dep = PersonsDetect.objects.filter(person_id__type_register='زائر')
    most_visitor_dep = most_visitor_dep.values('person_id','person_id__name','person_id__image','person_id__job_title')
    most_visitor_dep = most_visitor_dep.annotate(visits=Count('person_id__info__department'))
    most_visitor_dep = most_visitor_dep.order_by('-visits')[:5]

    return render(request, 'home/index.html', context={         
                                                       'active_Empolyee':activeEmpoly,
                                                       'most_visitor':most_visitor,
                                                       "most_visitor_dep":most_visitor_dep,
                                                       "most_empolyee":most_empolyee,
                                                       "most_visitor_after":most_visitor_after,
                                                       'active_visitor':active_visitor,
                                                       'all_visitor':all_visitor,
                                                       'active_visitor_after':active_visitor_after,
                                                       'cameras':cameras,
                                                       'counts_day_emp':counts_day_emp,
                                                       'counts_day_vis':counts_day_vis,
                                                       'counts_week_emp':counts_week_emp,
                                                       'counts_week_vis':counts_week_vis,
                                                       'counts_month_emp':counts_month_emp,
                                                       'counts_month_vis':counts_month_vis,
                                                       'counts_year_emp':counts_year_emp,
                                                       'counts_year_vis':counts_year_vis,
                                                       'departments':departments,
                                                       'counts_department':department_counts,
                                                       'total_deps':total_deps
                                                       })

def result_cameras(request):
    resu=copy.deepcopy(object_data)
    object_data.clear()
    return JsonResponse({
        "data": resu
    })


@login_required
def filter_camera(request, filter_date,camera_id):
    start_date_str, end_date_str = filter_date.split(" - ")
    start_date = datetime.strptime(start_date_str, "%B %d, %Y")
    end_date = datetime.strptime(end_date_str, "%B %d, %Y")
    detection_count = PersonsDetect.objects.filter(detected_at__range=(start_date, end_date),
                                                   camera_id__id=camera_id).count()
    detection_count_white = PersonsDetect.objects.filter(detected_at__range=(start_date, end_date),
                                                         camera_id__id=camera_id,
                                                         person_id__status='whitelist').count()
    detection_count_black = PersonsDetect.objects.filter(detected_at__range=(start_date, end_date),
                                                         camera_id__id=camera_id,
                                                         person_id__status='blacklist').count()
    detection_count_unknown = PersonsDetect.objects.filter(detected_at__range=(start_date, end_date),
                                                           camera_id__id=camera_id,
                                                           person_id__status='unknown').count()
    return JsonResponse({
        "detection_count": "detection_count",
        "detection_count_white": "detection_count_white",
        "detection_count_black": "detection_count_black",
        "detection_count_unknown": "detection_count_unknown"
    })

