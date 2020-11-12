from rest_framework import serializers

from .models import User
from djoser.serializers import UserCreateSerializer

class UserSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city')
    school_name = serializers.CharField(source='school')

    class Meta:
        model = User
        fields = (
            'psy_code',
            'first_name',
            'last_name',
            'email',
            'level',
            'city_name',
            'school_name'
        )


class UserListSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'psy_code',
            'full_name',
            'position',
            'phone',
            'email',
        )


class UserDetailSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name')
    school_name = serializers.CharField(source='school.name')
    class Meta:
        model = User
        fields = (
            'psy_code',
            'first_name',
            'last_name',
            'email',
            'level',
            'city_name',
            'school_name'
        )


class UserCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name
        )

        instance.last_name = validated_data.get(
            'last_name', instance.last_name
        )
        instance.email = validated_data.get('email', instance.email)
        instance.level = validated_data.get('level', instance.level)
        instance.city = validated_data.get('city', instance.city)
        instance.school = validated_data.get('school', instance.school)
        try:
            if not instance.check_password(validated_data.get('password')):
                instance.set_password(validated_data.get('password'))
        except:
            ...
        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'level',
            'city',
            'school',
            'password',
        )
