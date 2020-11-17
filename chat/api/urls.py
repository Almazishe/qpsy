from django.urls import path

from .  import views
from bot.bot import bot

# for i in range(10):
    # bot.send_message(914470745, 'PIDORAZ')


urlpatterns = [
    path('send-message', views.send_message, name='send-message'),
    path('chats', views.get_chats, name='chats'),
    path('messages', views.get_messages_list, name='messages'),
]
