from re import L
from rest_framework import serializers


from locations.models import School

from locations.city.serializers import CitySerializer

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = (
            'id',
            'code',
            'name',
            'city',
        )
    
    def to_representation(self, value):
       ret = super().to_representation(value)
       ret['city'] = CitySerializer(value.city).data
       return ret