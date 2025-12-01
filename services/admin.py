# from django.contrib import admin
# from .models import Service, ServiceImage, Package

# class ServiceImageInline(admin.TabularInline):
#     model = ServiceImage
#     extra = 0
#     max_num = 4

# class PackageInline(admin.TabularInline):
#     model = Package
#     extra = 0
#     min_num = 0
#     fields = ('name', 'price', 'duration_days', 'is_active')

# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ('title', 'operator', 'price', 'is_approved', 'is_active', 'created_at')
#     list_filter = ('is_approved', 'category', 'city', 'country')
#     inlines = [ServiceImageInline, PackageInline]


# @admin.register(Package)
# class PackageAdmin(admin.ModelAdmin):
#     list_display = ('name', 'service', 'price', 'is_active', 'created_at')
#     list_filter = ('is_active',)
#     search_fields = ('name', 'service__title')

from django.contrib import admin
from .models import Service, Package


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "price", "duration_days", "is_active")
    list_filter = ("is_active", "service")
    search_fields = ("name", "service__title")
    ordering = ("service", "name")
