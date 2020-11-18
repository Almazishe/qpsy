from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from locations.models import School
from .serializers import SchoolSerializer
from accounts.permissions import IsAdmin


class SchoolListView(ListAPIView):
    queryset = School.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated, 
        IsAdmin,
    )
    serializer_class = SchoolSerializer

class SchoolDetailView(RetrieveAPIView):
    lookup_field = 'code'
    queryset = School.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = SchoolSerializer

class SchoolDeleteView(DestroyAPIView):
    lookup_field = 'code'
    queryset = School.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = SchoolSerializer

class SchoolCreateView(CreateAPIView):
    queryset = School.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = SchoolSerializer

class SchoolUpdateView(UpdateAPIView):
    lookup_field = 'code'
    queryset = School.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = SchoolSerializer