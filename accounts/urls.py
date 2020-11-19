from accounts.views import change_status
from django.urls import path

from . import views

urlpatterns = [
    path('update-status', views.change_status),
    path('create', views.create_user),
    path('list', views.users_list),
    path('update-email', views.update_email),
]
