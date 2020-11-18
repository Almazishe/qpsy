from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated


from locations.models import Region
from .serializers import RegionSerializer
from accounts.permissions import IsAdmin

class RegionListView(ListAPIView):
    queryset = Region.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated, 
        IsAdmin,
    )
    serializer_class = RegionSerializer

class RegionDetailView(RetrieveAPIView):
    lookup_field = 'code'
    queryset = Region.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = RegionSerializer

class RegionDeleteView(DestroyAPIView):
    lookup_field = 'code'
    queryset = Region.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = RegionSerializer

class RegionCreateView(CreateAPIView):
    queryset = Region.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = RegionSerializer

class RegionUpdateView(UpdateAPIView):
    lookup_field = 'code'
    queryset = Region.objects.all().order_by('code')
    permission_classes = (
        IsAuthenticated,
        IsAdmin
    )
    serializer_class = RegionSerializer