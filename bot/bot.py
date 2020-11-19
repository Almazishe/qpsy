from chat.models import SENT
from chat.models import Message
import time
import telebot
import logging
from telebot import types
from .models import TelegramUser
from .models import ChatState
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

from .utils import get_tg_user


WEBHOOK_HOST = 'qpsy.herokuapp.com'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = f'https://{WEBHOOK_HOST}:{WEBHOOK_PORT}'
WEBHOOK_URL_PATH = '/bot/'


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(settings.BOT_TOKEN)

User = get_user_model()


reply_keyboard = [
    {'name': 'Написать сообщение психологу'},
    {'name': 'Горячая линия'},
]

# keyboard = reply_keyboard
#             key = types.ReplyKeyboardMarkup(True, False)
#             for i in range(len(keyboard)):
#                 but = types.KeyboardButton(keyboard[i]['name'])
#                 key.add(but)

#             bot.send_message(
#                 message.chat.id,
#                 text=f'Привет {tg_user.name}! =) , выбери что ты хотел бы сделать... ',
#                 reply_markup=key
#             )

@method_decorator(csrf_exempt, name='dispatch')
class BotView(View):
    def get(self, request):
        return HttpResponse('get')

    def post(self, request):
        if request.headers.get('Content-Type') == 'application/json':
            json_string = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
        return HttpResponse('post')



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        tg_user = get_tg_user(message.chat.id)
        if tg_user:
            bot.send_message(
                message.chat.id,
                text='У вас уже есть психолог' 
            )
        else:
            bot.send_message(message.chat.id,
                            ('Привет, введи код школьного психолога.'))
    except Exception as e:
        bot.send_message(
                message.chat.id,
                text='Ошибка в /start методе \n' + str(e) 
            )


# @bot.message_handler(content_types=['text'])
# def any_message(message):
#     data = get_tg_user(message.chat.id)
#     if data['status']:
#         tg_user = data['tg_user']
#         if message.text == reply_keyboard[1]['name']:
#             bot.send_message(
#                 message.chat.id,
#                 'Позвони тебе помогут\n' +
#                 '8-(776)-168-87-60'
#             )
#         elif message.text == reply_keyboard[0]['name']:
#             bot.send_message(
#                 message.chat.id,
#                 f'Напиши что угодно я обязательно тебе помогу {tg_user.name}'
#             )
#         else:
#             message = Message(
#                 tg_user=tg_user,
#                 text=message.text,
#                 status=SENT
#             )
#             message.save()
#     else:
#         bot.send_message(
#             message.chat.id, f'Введи команду /start, чтобы начать.')


bot.remove_webhook()
time.sleep(0.1)
bot.set_webhook(url=f'{WEBHOOK_URL_BASE}{WEBHOOK_URL_PATH}')




