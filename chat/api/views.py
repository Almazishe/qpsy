from bot.bot import bot
from chat.views import get_tg_user
from chat.models import Message
from chat.models import RECEIVED
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import get_user_model
Manager = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    response_data = {}
    if request.method == 'POST':
        data = request.data
        if 'clientID' in data and 'text' in data:
            tg_user = get_tg_user(data['clientID'])

            if tg_user:
                message = Message(
                    tg_user=tg_user,
                    status=RECEIVED,
                    text=data['text']
                )
                message.save()

                bot.send_message(
                    chat_id=tg_user.chat_id,
                    text=message.text
                )

                response_data['success'] = 'Message successfully sent to Telegram Client.'

                return Response(
                    data=response_data,
                    status=status.HTTP_201_CREATED
                )
            else:
                response_data['error'] = 'No Telegram Client with such ID.'
                return Response(
                    data=response_data,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            response_data['error'] = '\'clientID\' or \'text\' didn\'t came.'
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        response_data['error'] = 'Only \'POST\' requsts accepted.'
        return Response(
            data=response_data,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chats(request):
    ...
