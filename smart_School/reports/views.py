from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta, datetime
from app_resources.models import PersonsDetect, Cameras
# from livefeed.utils import search_by_image_unknown_filter, search_by_image_black_filter, search_by_image_all_filter, \
#     search_by_image_known_filter, search_by_image_white_filter
from reports.utils import filter_persons
from django.contrib.auth.decorators import login_required

from home.utils import perform_detection
@login_required
def report(request):
    return render(request,'reports/report.html')

def load_data(request, date):
    if 'to' in date:
        start, end = date.split('to')
        start_date = datetime.strptime(start.strip(), "%Y-%m-%d")
        end_date = datetime.strptime(end.strip(), "%Y-%m-%d")
        queryset = PersonsDetect.objects.filter(detected_at__date__range=(start_date, end_date))
    else:
        queryset = PersonsDetect.objects.filter(detected_at__date=datetime.strptime(date, "%Y-%m-%d"))
    data=perform_detection(queryset)
    return JsonResponse(data, safe=False)
