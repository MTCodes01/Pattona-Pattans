from django.urls import path
from . import views

urlpatterns = [
    path('initialize/', views.HardwareInitializationAPI.as_view(), name='initialize_hardware'),
    path('realtime-data/', views.RealTimeDataAPI.as_view(), name='realtime_data'),
    path('historical-data/', views.HistoricalDataAPI.as_view(), name='historical_data'),
    path('status/', views.HardwareStatusAPI.as_view(), name='hardware_status'),
    path('stop/', views.HardwareStopConnectionAPI.as_view(), name='stop_hardware'),
]
