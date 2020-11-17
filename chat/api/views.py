from chat.api.serializers import MessageListSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import get_user_model
Manager = get_user_model()

from bot.bot import bot

from chat.views import get_messages, get_tg_user
from chat.views import get_serialized_chats_list
from chat.models import Message
from chat.models import RECEIVED

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    response_data = {}
    if request.method == 'POST':
        data = request.data
        if 'clientID' in data and 'text' in data:
            tg_user = get_tg_user(data['clientID'])

            if tg_user:

                if tg_user.active_psy.psy_code == request.user.psy_code:
                    message = Message(
                        tg_user=tg_user,
                        status=RECEIVED,
                        text=data['text'],
                        is_read=True
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
                    response_data['error'] = 'It\'s not you Telegram Client.'
                    return Response(
                        data=response_data,
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                response_data['error'] = 'No Telegram Client with such ID.'
                return Response(
                    data=response_data,
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            response_data['error'] = '\'clientID\' or \'text\' didn\'t came.'
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        response_data['error'] = 'Only \'POST\' requests accepted.'
        return Response(
            data=response_data,
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chats(request):
    response_data = {}
    if request.method == 'GET':
        tg_users = request.user.active_students.all()
        serialized_data = get_serialized_chats_list(tg_clients=tg_users,  manager=request.user)
        response_data['chats'] = serialized_data
        response_data['success'] = 'Chats got successfully.'
        return Response(
            response_data,
            status=status.HTTP_200_OK
        )
    else:
        response_data['error'] = 'Only \'GET\' requests accepted.'
        return Response(
            data=response_data,
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages_list(request):
    response_data = {}
    if request.method == 'GET':
        tg_client_id = request.query_params.get('clientID', None)
        if tg_client_id is not None:
            tg_client = get_tg_user(tg_client_id=tg_client_id)

            if tg_client is not None:

                messages = get_messages(tg_client=tg_client)
                messages.update(is_read=True)

                serializer = MessageListSerializer(messages, many=True)
                response_data['client'] = {
                    'id': tg_client.id,
                    'name': tg_client.name
                }
                response_data['messages'] = serializer.data
                response_data['success'] = 'Messages got successfully.'
                return Response(
                    response_data,
                    status=status.HTTP_200_OK,
                )
            else:
                response_data['error'] = 'No Telegram Client with such ID.'
                return Response(
                    data=response_data,
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            response_data['error'] = '\'clientID\'  didn\'t came.'
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        response_data['error'] = 'Only \'GET\' requests accepted.'
        return Response(
            data=response_data,
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )



