from rest_framework import serializers

from chat.models import Message


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'text',
            'timestamp'
        )

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'