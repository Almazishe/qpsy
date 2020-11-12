from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse 
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import TelegramUser

from telebot import types

import logging
import telebot
import time


WEBHOOK_HOST = 'qpsy.herokuapp.com'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = f'https://{WEBHOOK_HOST}:{WEBHOOK_PORT}'
WEBHOOK_URL_PATH = '/bot/'


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(settings.BOT_TOKEN)
    
from django.contrib.auth import get_user_model
User = get_user_model()

reply_keyboard = [
    {'name': 'Написать сообщение психологу'},
    {'name': 'Горячая линия'},
]

def create_tg_user(message, psy):
    try:
        tg_user = TelegramUser.objects.get_or_create(
            chat_id = message.chat.id,
            defaults={
                'main_psy': psy,
                'active_psy': psy,
            },
        )

        return tg_user
    except:
        return None

def get_tg_user(chat_id):
    res = {}
    try:
        tg_user = TelegramUser.objects.get(chat_id=chat_id)
        res['tg_user'] = tg_user
        res['status'] = True 
        return res
    except:
        res['status'] = False
        return res

def get_psy(code):
    code = int(code)
    res = {}
    try:
        psy = User.objects.get(psy_code=code)
        res['psy'] = psy
        res['status'] = True 
        return res
    except:
        res['status'] = False
        return res

def is_exist(chat_id):
    try:
        tg_user = TelegramUser.objects.get(chat_id=chat_id)
        return True
    except:
        return False



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


def wait_for_code(message):
    try:
        data = get_psy(message.text)

        if not data['status']:
            msg = bot.send_message(
                message.chat.id,
                text='Нет школьного психолога с данным кодом. \n\n Пожалуйста перевведи код.'
            )

            bot.register_next_step_handler(msg, wait_for_code)
        else:
            tg_user = create_tg_user(message=message, psy=data['psy'])

            if tg_user:
                msg = bot.send_message(
                    message.chat.id,
                    text='Как к тебе обращаться? =) \n Можешь не вводить настоящего имени (Например: \'Друг\').'
                )

                bot.register_next_step_handler(msg, wait_for_name)
            else:
                msg = bot.send_message(
                    message.chat.id,
                    text = 'Что-то пошло не так... \n\n Пожалуйста перевведи код.'
                )

                bot.register_next_step_handler(msg, wait_for_code)
    except Exception as e:
        msg = bot.send_message(
            message.chat.id,
            text = 'Что-то пошло не так... \n\n Пожалуйста перевведи код. ' + str(e)
        )

        bot.register_next_step_handler(msg, wait_for_code)

def wait_for_name(message):
    try:
        data = get_tg_user(message.chat.id)

        if data['status']:
            tg_user = data['tg_user']
            tg_user.name = message.text
            tg_user.save()

            keyboard = reply_keyboard
            key = types.ReplyKeyboardMarkup(True, False)
            for i in range(len(keyboard)):
                but = types.KeyboardButton(keyboard[i]['name'])
                key.add(but)
            


            bot.send_message(
                message.chat.id,
                text = f'Привет {tg_user.name}! =) , выбери что ты хотел бы сделать... ',
                reply_markup = key
            )


        else:
            msg = bot.send_message(
                message.chat.id,
                text = 'Что-то пошло не так... \n\n Пожалуйста перевведи имя.'
            )

            bot.register_next_step_handler(msg, wait_for_name)
    except Exception as e:
        msg = bot.send_message(
            message.chat.id,
            text = 'Что-то пошло не так... \n\n Пожалуйста перевведи имя. ' + str(e)
        )

        bot.register_next_step_handler(msg, wait_for_name)






@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id,
                ('Привет, введи код школьного психолога.'))

    bot.register_next_step_handler(msg, wait_for_code)
    

@bot.message_handler(content_types=['text'])
def any_message(message):
    data = get_tg_user(message.chat.id)
    if data['status']:
        tg_user = data['tg_user']
        if message.text == reply_keyboard[1]['name']:
            bot.send_message(
                message.chat.id,
                'Позвони тебе помогут\n' + \
                '8-(776)-168-87-60'
            )
        elif message.text == reply_keyboard[0]['name']:
            bot.send_message(
                message.chat.id,
                f'Напиши что угодно я обязательно тебе помогу {tg_user.name}'
            )
        else:
            bot.send_message(
                message.chat.id,
                f'{tg_user.name} ты написал: \n - {message.text}'
            )
    else:
        bot.send_message(message.chat.id, f'Введи команду /start, чтобы начать.')
    



bot.remove_webhook()
time.sleep(0.1)
bot.set_webhook(url=f'{WEBHOOK_URL_BASE}{WEBHOOK_URL_PATH}')