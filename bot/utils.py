from django.shortcuts import get_object_or_404
from bot.models import TelegramUser


def get_tg_user(chat_id):
    tg_user = get_object_or_404(TelegramUser, chat_id=chat_id)
    return tg_user



# def create_tg_user(chat_id):
