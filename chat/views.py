from bot.models import TelegramUser
from django.shortcuts import get_object_or_404


def get_tg_user(tg_client_id):
    tg_client = get_object_or_404(TelegramUser, id=tg_client_id)
    return tg_client
