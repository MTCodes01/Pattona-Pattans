from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('initialize/', views.InitializationAPI.as_view(), name='initialize'),
    path('database/', views.DatabaseExplorerAPI.as_view(), name='database-explorer'),
    path('usage/', views.UsageAPI.as_view(), name='usage'),
    path('switch/', views.SwitchAPI.as_view(), name='switch'),
    path('device-status/', views.DeviceStatusAPI.as_view(), name='device_status'),
    path('notifications/', views.NotificationsAPI.as_view(), name='notifications'),
    path('analytics/', views.AnalyticsAPI.as_view(), name='analytics'),
    path('schedules/', views.SchedulesAPI.as_view(), name='schedules'),
    path('schedules/<int:schedule_id>/', views.SchedulesAPI.as_view(), name='schedule_delete'),
]
