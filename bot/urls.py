from django.urls import path

from .bot import BotView

urlpatterns = [
    path('bot/', BotView.as_view(), name='bot')
]
