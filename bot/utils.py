from django.shortcuts import get_object_or_404
from bot.models import TelegramUser
from bot.models import ChatState
from chat.models import Message
from chat.models import SENT
from django.contrib.auth import get_user_model
User = get_user_model()

def send_message(tg_user, text):
    message = Message.objects.create(
        tg_user=tg_user,
        text=text,
        status=SENT
    )

    return message


def create_tg_user(chat_id, psy):
    tg_user = TelegramUser.objects.create(
        chat_id=chat_id,
        main_psy=psy,
        active_psy=psy
    )
    return tg_user

def get_psy(code):
    psy = get_object_or_404(User,  psy_code=code)
    return psy

def get_tg_user(chat_id):
    tg_user = get_object_or_404(TelegramUser, chat_id=chat_id)
    return tg_user

def get_or_create_current_state(chat_id):
    try:
        chat_state = ChatState.objects.get(chta_id=chat_id)
    except:
        chat_state = ChatState.objects.create(
            chat_id=chat_id,
            state=0
        )
    return chat_state


