
from rest_framework import serializers
from .models import Building, Meters, MetersReadings

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class MetersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meters
        fields = '__all__'

class MetersReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetersReadings
        fields = '__all__'
        