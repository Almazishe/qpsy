from rest_framework import serializers

from .models import City, Region, School


class RegionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = (
            'code',
            'name'
        )

class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'code',
            'name',
            'region'
        )


class SchoolDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = (
            'code',
            'name',
            'city'
        )