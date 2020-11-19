from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from rest_framework.permissions import IsAuthenticated

from .serializers import UserCreateSerializer
from .serializers import AdminUsersSerializer
from .permissions import IsAdmin
from .permissions import IsSpecialist
from .permissions import SelfOrAdmin
from .models import SPECIALIST, PSYCHOLOGIST
LEVELS = [SPECIALIST, PSYCHOLOGIST]
from .models import ONLINE
from .models import OFFLINE


from .utils import normalize_email

from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated, SelfOrAdmin])
def change_status(request):
    response_data = {}
    if request.method == 'POST':
        if request.user.status == ONLINE:
            request.user.status = OFFLINE
            request.user.save()
        else:
            request.user.status = ONLINE
            request.user.save()  
        response_data['success'] = 'Status changed successfully.'
        response_data['status'] = request.user.status
        return Response(
            data=response_data,
            status=status.HTTP_200_OK
        )
    else:
        response_data['error'] = 'Only POST request\'s accepted.'

    return Response(
        data=response_data,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated, SelfOrAdmin])
def update_email(request):
    response_data = {}
    if request.method == 'POST':
        data = request.data
        if 'email' in data:
            try:
                user = request.user 
                email = normalize_email(data['email'])
                user.email = email
                user.save()

                response_data['success'] = 'Email changed successfully.'
                return Response(
                    data=response_data,
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:
                response_data['error'] = 'Email not correct format. Must be <email_name>@<domain_part>'
                return Response(
                    data=response_data,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            response_data['error'] = 'No email in data body.'
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        response_data['error'] = 'Only POST request\'s accepted.'

    return Response(
        data=response_data,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def create_user(request):
    ''' ADMIN CREATES USER '''
    response_data = {}
    if request.method == 'POST':
        serializer = UserCreateSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            user = serializer.save()
            response_data['message'] = 'Пользователь успешно создан.'
            response_data['user'] = {
                'id': user.id,
                'code': user.psy_code,
                'full_name': user.get_full_name(),
                'email': user.email
            }
            return Response(
                data=response_data,
                status=status.HTTP_201_CREATED
            )
        else:
            response_data = serializer.errors
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        response_data['error'] = 'Only POST request\'s accepted.'

    return Response(
        data=response_data,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def users_list(request):
    response_data = {}
    if request.method == 'GET':
        users = User.objects.filter(level__in=LEVELS)
        serializer = AdminUsersSerializer(users, many=True)
        response_data['users'] = serializer.data

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )
    else:
        response_data['error'] = 'Only GET request\'s accepted.'

    return Response(
        data=response_data,
        status=status.HTTP_400_BAD_REQUEST
    )
