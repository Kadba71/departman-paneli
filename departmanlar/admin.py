from django.contrib import admin
from .models import DataRecord, ManagerBonus, Contact, BulkMessage

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

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "department", "is_active", "created_at")
    list_filter = ("is_active", "department", "created_at")
    search_fields = ("name", "phone_number", "department")
    list_per_page = 20
    date_hierarchy = 'created_at'

@admin.register(BulkMessage)
class BulkMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "message_content_preview", "total_recipients", "success_count", "failed_count", "sent_at")
    list_filter = ("sent_at", "sender")
    search_fields = ("message_content", "sender__username")
    readonly_fields = ("sent_at", "total_recipients", "success_count", "failed_count")
    list_per_page = 20
    date_hierarchy = 'sent_at'
    
    def message_content_preview(self, obj):
        return obj.message_content[:50] + "..." if len(obj.message_content) > 50 else obj.message_content
    message_content_preview.short_description = "Mesaj İçeriği"