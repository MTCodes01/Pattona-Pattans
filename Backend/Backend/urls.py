from django.contrib import admin
from django.urls import path, include
from Ecox import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('Ecox/', include('Ecox.urls')),
    path('Hardware/', include('Hardware.urls')),
]
