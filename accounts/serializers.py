from rest_framework import serializers

from .models import User

from locations.serializers import AdminCityDetailSerializer
from locations.serializers import AdminSchoolDetailSerializer


class AdminUsersSerializer(serializers.ModelSerializer):
    school = AdminSchoolDetailSerializer()
    city = AdminCityDetailSerializer()
    class Meta:
        model = User
        fields = (
            'id',
            'psy_code',
            'email',
            'first_name',
            'last_name',
            'level',
            'city',
            'school',
        )

class UserSerializer(serializers.ModelSerializer):
    
    city_name = serializers.CharField(source='city.name', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)
    level = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name
        )

        instance.last_name = validated_data.get(
            'last_name', instance.last_name
        )
        instance.email = validated_data.get('email', instance.email)

        if self.context['request'].user.is_superuser:
            instance.level = validated_data.get('level', instance.level)
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
            'psy_code',
            'first_name',
            'last_name',
            'email',
            'level',
            'city_name',
            'school_name',
            'status'
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

        if self.context['request'].user.is_superuser:
            instance.level = validated_data.get('level', instance.level)
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
