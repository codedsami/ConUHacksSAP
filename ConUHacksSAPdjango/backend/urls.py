from django.urls import path
from . import views

urlpatterns = [
        path('optimize/', views.optimize_resources, name='optimize_resources'),
        path('fire_events/', views.get_fire_events, name='get_fire_events'),
        path('resources/', views.get_resources, name='get_resources'),
]