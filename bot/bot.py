from telebot.apihelper import send_message
from chat.models import SENT
from chat.models import Message
import time
import telebot
import logging
from telebot import types
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

from .utils import get_psy
from .utils import get_tg_user
from .utils import send_message
from .utils import create_tg_user
from .utils import get_or_create_current_state


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
        bot.send_message(
            message.chat.id,
            text='У вас уже есть психолог' 
        )
    except Exception as e:
        chat_state = get_or_create_current_state(message.chat.id)
        if chat_state.state == 0:
            chat_state.state = 1
            chat_state.save()
            bot.send_message(message.chat.id,  ('Привет, введи код школьного психолога.'))


@bot.message_handler(func=lambda message: get_or_create_current_state(message.chat.id).state == 1,  content_types=['text'])
def wait_code(message):
    try:
        chat_id = message.chat.id
        psy = get_psy(message.text)
        tg_user = create_tg_user(chat_id, psy)

        chat_state = get_or_create_current_state(chat_id)
        chat_state.state = 2
        chat_state.save()

        bot.send_message(message.chat.id,  ('Как к тебе обращаться? \nPS: Можешь ввести любое имя =) '))
    except:
        bot.send_message(message.chat.id,  'Психолога с таким кодом увы не существует, попробуй снова ввести код.')

@bot.message_handler(func=lambda message: get_or_create_current_state(message.chat.id).state == 2, content_types=['text'])
def wait_name(message):
    try:
        chat_id = message.chat.id
        chat_state = get_or_create_current_state(chat_id)

        tg_user = get_tg_user(chat_id)
        tg_user.name = message.text
        tg_user.save()

        chat_state.state = 3
        chat_state.save()

        keyboard = reply_keyboard
        key = types.ReplyKeyboardMarkup(True, False)
        for i in range(len(keyboard)):
            but = types.KeyboardButton(keyboard[i]['name'])
            key.add(but)

        bot.send_message(
            chat_id,
            text=f'Привет {tg_user.name}! =) , меня зовут {tg_user.active_psy.first_name} {tg_user.active_psy.last_name} Выбери что ты хотел бы сделать или же можешь просто начать печатать я обязательно отвечу тебе =) ',
            reply_markup=key
        )
    except Exception as e:
        bot.send_message(message.chat.id,  f'ERROR[wait_name]: {str(e)}')


@bot.message_handler(func=lambda message: get_or_create_current_state(message.chat.id).state == 3, content_types=['text'])
def chat(message):
    chat_id = message.chat.id
    try:
        tg_user = get_tg_user(chat_id)
        if message.text == reply_keyboard[1]['name']:
            bot.send_message(
                message.chat.id,
                'Позвони тебе помогут\n' +
                '8-(776)-168-87-60'
            )
        elif message.text == reply_keyboard[0]['name']:
            bot.send_message(
                message.chat.id,
                f'Напиши что угодно я обязательно тебе помогу {tg_user.name}'
            )
        else:
            send_message(tg_user, message.text)
    except:
        bot.send_message(message.chat.id,  f'ERROR[chat]: {str(e)}')
        
    

# @bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_AGE.value)
# def user_entering_age(message):
#     # А вот тут сделаем проверку
#     if not message.text.isdigit():
#         # Состояние не меняем, поэтому только выводим сообщение об ошибке и ждём дальше
#         bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
#         return
#     # На данном этапе мы уверены, что message.text можно преобразовать в число, поэтому ничем не рискуем
#     if int(message.text) < 5 or int(message.text) > 100:
#         bot.send_message(message.chat.id, "Какой-то странный возраст. Не верю! Отвечай честно.")
#         return
#     else:
#         # Возраст введён корректно, можно идти дальше
#         bot.send_message(message.chat.id, "Когда-то и мне было столько лет...эх... Впрочем, не будем отвлекаться. "
#                                           "Отправь мне какую-нибудь фотографию.")
#         dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)


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




