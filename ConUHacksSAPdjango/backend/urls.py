from django.urls import path
from . import views

urlpatterns = [
        path('optimize/', views.optimize_resources, name='optimize_resources'),
        path('fire_events/', views.get_fire_events, name='get_fire_events'),
        path('resources/', views.get_resources, name='get_resources'),
        path('upload/fire_events/', views.upload_fire_events, name='upload_fire_events'),
        path('allocate/resources/', views.upload_resources, name='upload_resources'),
]