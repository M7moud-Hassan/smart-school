from django.urls import path
from .views import *
urlpatterns = [
   path('all/',reports_all_people,name="reports_all_people"),
   path('unknown/',reports_known_people,name='reports_known_people'),
   path('white/',reports_white_people,name='reports_white_people'),
   path('black/',reports_black_people,name='reports_black_people'),
   path('reports_unknown_people/',reports_unknown_people,name='reports_unknown_people'),
]
