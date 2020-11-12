from .models import Region, City, School

from django.contrib import admin

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'region')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city')