from django.urls import path
from . import views

urlpatterns = [
        path('optimize/', views.optimize_resources, name='optimize_resources'),
        path('fire_events/', views.get_fire_events, name='get_fire_events'),
        path('resources/', views.get_resources, name='get_resources'),
        path('predict/', views.get_predicted_fire_events, name='get_predicted_fire_events'),
        path('upload/current_fire_events/', views.upload_current_fire_events, name='upload_fire_events'),
        path('upload/historical_fire_events/', views.upload_historical_fire_events, name='upload_historical_fire_events'),
]