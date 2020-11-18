from re import L
from rest_framework import serializers


from locations.models import City

from locations.region.serializers import RegionSerializer


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'code',
            'name',
            'region'
        )
    
    def to_representation(self, value):
       ret = super().to_representation(value)
       ret['region'] = RegionSerializer(value.region).data
       return ret