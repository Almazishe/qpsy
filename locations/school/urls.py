from django.urls import path

from . import views

urlpatterns = [
    path('list', views.SchoolListView.as_view()),
    path('create', views.SchoolCreateView.as_view()),
    path('detail/<code>', views.SchoolDetailView.as_view()),
    path('update/<code>', views.SchoolUpdateView.as_view()),
    path('delete/<code>', views.SchoolDeleteView.as_view()),
]
