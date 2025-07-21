from django.contrib import admin
from .models import Departman, Veri

@admin.register(Departman)
class DepartmanAdmin(admin.ModelAdmin):
    list_display = ("isim",)
    search_fields = ("isim",)

@admin.register(Veri)
class VeriAdmin(admin.ModelAdmin):
    list_display = ("departman", "baslik", "deger", "tarih")
    list_filter = ("departman", "baslik")
    search_fields = ("baslik", "deger")
    list_per_page = 20