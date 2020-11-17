from django.db.models import fields
from rest_framework import serializers

from .models import TelegramUser

class TelegtramUsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'