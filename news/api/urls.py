from django.urls import path

from . import views

urlpatterns = [
    path('list', views.NewsListView.as_view()),
    path('create', views.NewsCreateView.as_view()),
    path('detail/<pk>', views.NewsDetailView.as_view()),
    path('update/<pk>', views.NewsUpdateView.as_view()),
    path('delete/<pk>', views.NewsDeleteView.as_view()),
]
