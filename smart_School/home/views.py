import copy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from app_resources.utils import object_data
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta, datetime
from datetime import date
from app_resources.models import Persons, PersonsDetect, Cameras
from dashboard.models import Department
from django.db.models import Count


# Create your views here.
@login_required
def index(request):
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    this_month_start = today.replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    this_year_start = today.replace(month=1, day=1)
    last_year_start = this_year_start.replace(year=this_year_start.year - 1)
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
            person_id__type_register='Employee'
        ).count()
        count2 = PersonsDetect.objects.filter(
            detected_at__gte=start_time,
            detected_at__lt=end_time,
            person_id__type_register='Visitor'
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
            person_id__type_register='Employee'
        ).count()
        count2 = PersonsDetect.objects.filter(
            detected_at__date__gte=start_date,
            detected_at__date__lt=end_date,
            person_id__type_register='Visitor'
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
            person_id__type_register='Employee'
        ).count()
        count2 = PersonsDetect.objects.filter(
            detected_at__date__gte=start_date,
            detected_at__date__lt=end_date,
            person_id__type_register='Visitor'
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
            person_id__type_register='Employee'
        ).count()
        count2 = PersonsDetect.objects.filter(
            detected_at__date__gte=start_date,
            detected_at__date__lt=end_date,
            person_id__type_register='Visitor'
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
    registers = Persons.objects.filter(Q(status='whitelist') | Q(status='blacklist'))
    detectPersons = PersonsDetect.objects.filter(person_id__status="unknown")
    totalEmpolyees=Persons.objects.filter(type_register='Employee')
    totalVisitor=Persons.objects.filter(type_register='Visitor')
    # today = date.today()

    # Filter the PersonsDetect model for records detected today
    # persons_result = PersonsDetect.objects.filter(detected_at__date=today)
    return render(request, 'home/index.html', context={"registers": registers.count(),
                                                       "unknownDetect": detectPersons.count(),
                                                       'empolyees':totalEmpolyees,
                                                       'visitors':totalVisitor,
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

