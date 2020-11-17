from django.shortcuts import get_object_or_404

from bot.models import TelegramUser
from .models import Message
from .models import SENT


def get_tg_user(tg_client_id):
    tg_client = get_object_or_404(TelegramUser, id=tg_client_id)
    return tg_client

def get_messages(tg_client):
    messages = Message.objects.filter(tg_user=tg_client)
    return messages

def get_uread_messages_count(tg_client):
    return Message.objects.filter(
        tg_user=tg_client,
        status=SENT,
        is_read=False
    ).count()


def get_last_message(tg_client):
    try:
        result = Message.objects.filter(
            tg_user=tg_client,
        ).last().text
        return result
    except:
        return '...'


def get_serialized_chats_list(tg_clients, manager):
    response_data = []
    for tg_client in tg_clients:
        data = {}
        data['id'] = tg_client.id
        data['name'] = tg_client.name

        unread = get_uread_messages_count(tg_client=tg_client)
        data['unread'] = unread

        last_message = get_last_message(tg_client=tg_client)
        data['last_message'] = last_message

        response_data.append(data)
    return response_data
