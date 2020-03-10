from rest_framework import serializers
from .models import Building, Meters, MetersReadings

class BuildingSerializer(serializers.ModelSerializer):
	meters = serializers.SerializerMethodField()

	class Meta:
		model = Building
		fields = '__all__'

	def get_meters(self, obj):
		result = []
		for meter in obj.meters.all().order_by('fuel'):
			result.append({"fuel": meter.fuel, "meter_id": meter.meter_id})
		return result

class MetersSerializer(serializers.ModelSerializer):
	building_id = serializers.IntegerField(read_only=True, source="building.building_id")

	class Meta:
		model = Meters
		fields = '__all__'

class DetailMetersSerializer(MetersSerializer):
	readings = serializers.SerializerMethodField()

	class Meta(MetersSerializer.Meta):
		fields = ("fuel", "meter_id", "readings")

	def get_readings(self, obj):
		result = []
		for read in obj.readings.all():
			result.append({"consumption": read.consumption, "reading_date_time": read.reading_date_time})
		return result

class MetersReadingsSerializer(serializers.ModelSerializer):
	# meter_id = serializers.IntegerField(read_only=True, source="meter.meter_id")
	# building_id = serializers.IntegerField(read_only=True, source="meter.building.building_id")
	# fuel = serializers.CharField(read_only=True, source="meter.fuel")

	class Meta:
		model = MetersReadings
		fields = ("consumption", "reading_date_time")