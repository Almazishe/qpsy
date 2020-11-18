from django.urls import path

from . import views

urlpatterns = [
    path('list', views.CityListView.as_view()),
    path('create', views.CityCreateView.as_view()),
    path('detail/<code>', views.CityDetailView.as_view()),
    path('update/<code>', views.CityUpdateView.as_view()),
    path('delete/<code>', views.CityDeleteView.as_view()),
]
