from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from .serializers import UserCreateSerializer
from .permissions import IsAdmin
from .permissions import IsSpecialist
from .permissions import SelfOrAdmin


from django.contrib.auth import get_user_model
User = get_user_model()


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
