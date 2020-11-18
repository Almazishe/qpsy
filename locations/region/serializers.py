from re import L
from rest_framework import serializers


from locations.models import Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = (
            'id',
            'code',
            'name'
        )