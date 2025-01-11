from django.urls import path
from . import views

urlpatterns = [
    path('hardware/initialize/', views.HardwareInitializationAPI.as_view(), name='initialize_hardware'),
    path('hardware/realtime-data/', views.RealTimeDataAPI.as_view(), name='realtime_data'),
    path('hardware/historical-data/', views.HistoricalDataAPI.as_view(), name='historical_data'),
    path('hardware/status/', views.HardwareStatusAPI.as_view(), name='hardware_status'),
    path('hardware/stop/', views.HardwareStopConnectionAPI.as_view(), name='stop_hardware'),
]
