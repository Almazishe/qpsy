from django.urls import path

from . import views

urlpatterns = [
    path('list', views.RegionListView.as_view()),
    path('create', views.RegionCreateView.as_view()),
    path('detail/<code>', views.RegionDetailView.as_view()),
    path('update/<code>', views.RegionUpdateView.as_view()),
    path('delete/<code>', views.RegionDeleteView.as_view()),
]
