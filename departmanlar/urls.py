# filepath: c:\Users\kadir\OneDrive\Masaüstü\call.py\departmanlar\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('delete_data/<int:pk>/', views.delete_data, name='delete_data'),
    path('edit_data/<int:pk>/', views.edit_data, name='edit_data'),
    path('delete_bonus/<int:pk>/', views.delete_bonus, name='delete_bonus'),
    path('edit_bonus/<int:pk>/', views.edit_bonus, name='edit_bonus'),
    path('export_data/', views.export_data, name='export_data'),
]