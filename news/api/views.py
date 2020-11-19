from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsSpecialist
from accounts.paginations import CustomPagination
from news.models import News

from .serializers import NewsSerializer



class NewsListView(ListAPIView):
    queryset = News.objects.all()
    permission_classes = (
        IsAuthenticated, 
    )
    pagination_class = CustomPagination
    serializer_class = NewsSerializer

class NewsDetailView(RetrieveAPIView):
    queryset = News.objects.all()
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = NewsSerializer

class NewsDeleteView(DestroyAPIView):
    queryset = News.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsSpecialist
    )
    serializer_class = NewsSerializer

class NewsCreateView(CreateAPIView):
    queryset = News.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsSpecialist
    )
    serializer_class = NewsSerializer

class NewsUpdateView(UpdateAPIView):
    queryset = News.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsSpecialist
    )
    serializer_class = NewsSerializer

