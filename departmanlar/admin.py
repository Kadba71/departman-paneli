from django.contrib import admin
from .models import DataRecord, ManagerBonus

@admin.register(DataRecord)
class DataRecordAdmin(admin.ModelAdmin):
    list_display = ("department", "manager_name", "data_type", "title", "value", "date")
    list_filter = ("department", "manager_name", "data_type", "title")
    search_fields = ("title", "manager_name", "department")
    list_per_page = 20

@admin.register(ManagerBonus)
class ManagerBonusAdmin(admin.ModelAdmin):
    list_display = ("department", "manager_name", "info_title", "value", "month", "year")
    list_filter = ("department", "manager_name", "info_title", "month", "year")
    search_fields = ("manager_name", "info_title", "department")
    list_per_page = 20