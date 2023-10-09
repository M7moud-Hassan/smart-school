import copy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from app_resources.utils import object_data
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta, datetime

from app_resources.models import Persons, PersonsDetect, Cameras


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
    registers = Persons.objects.filter(Q(status='whitelist') | Q(status='blacklist'))
    detectPersons = PersonsDetect.objects.filter(person_id__status="unknown")

    detection_count = PersonsDetect.objects.filter(detected_at=today,
                                                   camera_id__id=cameras.first().id if cameras.first() else 0).count()
    detection_count_white = PersonsDetect.objects.filter(detected_at=today,
                                                         camera_id__id=cameras.first().id if cameras.first() else 0,
                                                         person_id__status='whitelist').count()
    detection_count_black = PersonsDetect.objects.filter(detected_at=today,
                                                         camera_id__id=cameras.first().id if cameras.first() else 0,
                                                         person_id__status='blacklist').count()
    detection_count_unknown = PersonsDetect.objects.filter(detected_at=today,
                                                           camera_id__id=cameras.first().id if cameras.first() else 0,
                                                           person_id__status='unknown').count()
    return render(request, 'home/index.html', context={"registers": registers.count(),
                                                       "unknownDetect": detectPersons.count(),
                                                       'today': PersonsDetect.objects.filter(
                                                           detected_at__date=today).count(),
                                                       'yesterday': PersonsDetect.objects.filter(
                                                           detected_at__date=yesterday).count(),
                                                       'this_month': PersonsDetect.objects.filter(
                                                           detected_at__date__range=[this_month_start, today]).count(),
                                                       'last_month': PersonsDetect.objects.filter(
                                                           detected_at__date__range=[last_month_start,
                                                                                     last_month_end]).count(),
                                                       'this_year': PersonsDetect.objects.filter(
                                                           detected_at__date__range=[this_year_start, today]).count(),
                                                       'last_year': PersonsDetect.objects.filter(
                                                           detected_at__date__range=[last_year_start,
                                                                                     last_year_start.replace(
                                                                                         year=last_year_start.year + 1,
                                                                                         day=1) - timedelta(
                                                                                         days=1)]).count(),
                                                       "cameras": cameras, "detection_count": detection_count,
                                                       "detection_count_white": detection_count_white,
                                                       "detection_count_black": detection_count_black,
                                                       "detection_count_unknown": detection_count_unknown,
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

