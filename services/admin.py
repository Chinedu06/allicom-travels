from django.contrib import admin
from .models import Service, ServiceImage, Package

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 0
    max_num = 4

class PackageInline(admin.TabularInline):
    model = Package
    extra = 0
    min_num = 0
    fields = ('name', 'price', 'duration_days', 'is_active')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'operator', 'price', 'is_approved', 'is_active', 'created_at')
    list_filter = ('is_approved', 'category', 'city', 'country')
    inlines = [ServiceImageInline, PackageInline]


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'service__title')
