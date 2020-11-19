from django.contrib import admin


from .models import TelegramUser
from .models import ChatState

admin.site.register(ChatState)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'active_psy')