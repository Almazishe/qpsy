from django.urls import path

from .  import views


urlpatterns = [
    path('send-message', views.send_message, name='send-message'),
    path('chats', views.get_chats, name='chats'),
    path('messages', views.get_messages_list, name='messages'),
]
