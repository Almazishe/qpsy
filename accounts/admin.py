from .models import User

from django.contrib import admin

@admin.register(User)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('psy_code', 'email')

