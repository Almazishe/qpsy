from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from locations.models import City
from .serializers import CitySerializer
from accounts.permissions import IsAdmin


class CityListView(ListAPIView):
    queryset = City.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated, 
        IsAdmin,
    )
    serializer_class = CitySerializer

class CityDetailView(RetrieveAPIView):
    lookup_field = 'code'
    queryset = City.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = CitySerializer

class CityDeleteView(DestroyAPIView):
    lookup_field = 'code'
    queryset = City.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = CitySerializer

class CityCreateView(CreateAPIView):
    queryset = City.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = CitySerializer

class CityUpdateView(UpdateAPIView):
    lookup_field = 'code'
    queryset = City.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = CitySerializer