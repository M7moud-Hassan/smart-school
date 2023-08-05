from django.http import JsonResponse
from django.shortcuts import render
from livefeed.utils import object_data


# Create your views here.

def index(request):
    return render(request, 'home/index.html')


def result_cameras(request):
    return JsonResponse({
        "data":object_data
    })
