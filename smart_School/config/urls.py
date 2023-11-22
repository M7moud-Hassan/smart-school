from django.urls import path
from .views import *
urlpatterns = [
    path('add_files/',add_files,name='add_files'),
    path('result_files/',result_files,name='result_files'),
    path('config/',importatnted_fileds,name='importatnted_fileds'),
    path('sheftat/',sheftat,name='sheftat'),
    path('add_sheftat/',add_sheftat,name='add_sheftat'),
    path('edit_sheft/<int:pk>/',edit_sheft,name='edit_sheft'),
    path('delete_sheft/<int:pk>/',delete_sheft,name='delete_sheft'),
    path('when_add/',when_add,name='when_add'),
    path('reasons/',reasons,name='reasons'),
    path('update_reason/<int:pk>/',update_reason,name='update_reason'),
    path('delete_reason/<int:pk>/',delete_reason,name='delete_reason'),
    path('add_duration/',add_duration,name='add_duration'),
    path('durations/',durations,name='durations'),
    path('update_duration/<int:pk>/',update_duration,name='update_duration'),
    path('delete_duration/<int:pk>/',delete_duration,name='delete_duration'),
]