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
    # Bulk messaging URLs
    path('bulk_message/', views.bulk_message_panel, name='bulk_message_panel'),
    path('delete_contact/<int:pk>/', views.delete_contact, name='delete_contact'),
    path('edit_contact/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('message_status/<int:message_id>/', views.message_status, name='message_status'),
]