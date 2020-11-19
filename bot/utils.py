from django.shortcuts import get_object_or_404
from bot.models import TelegramUser
from bot.models import ChatState


def get_tg_user(chat_id):
    tg_user = get_object_or_404(TelegramUser, chat_id=chat_id)
    return tg_user

def get_or_create_current_state(chat_id):
    chat_state = ChatState.objects.get_or_create(
        chat_id=chat_id,
        defaults=[
            state=0,
        ]
    )
    return chat_state.state


# def create_tg_user(chat_id):
