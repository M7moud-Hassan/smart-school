from django.http import JsonResponse
from django.shortcuts import render
from datetime import  datetime
from app_resources.models import PersonsDetect
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
    data=perform_detection(queryset,include=True)
    return JsonResponse(data, safe=False)
