from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('departman_paneli.departmanlar.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Bu satır mutlaka olmalı!
]