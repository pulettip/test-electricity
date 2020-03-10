from django.shortcuts import render
import csv
import json

from dateutil.parser import parse
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from itertools import islice

from .models import Building, Meters, MetersReadings
from .serializers import BuildingSerializer, MetersSerializer, DetailMetersSerializer, MetersReadingsSerializer

class BuildingViewSet(viewsets.ModelViewSet):
	model = Building
	serializer_class = BuildingSerializer
	# queryset = Building.objects.all().order_by('building_id')
	queryset = Building.objects.all()

	def get_queryset(self):
		qs = super().get_queryset()
		query = self.request.GET.get('q')

		if query is None:
			return qs

		filtered_qs=qs.filter(name__icontains=query)
		return filtered_qs

	def create(self, request):
		file = request.FILES["file"]
		file_data = file.read().decode("utf-8")
		lines = file_data.split("\n")
		i = 0
		new = 0
		existing = 0
		format_error = 0
		for line in lines:
			fields = line.split(",")
			
			if len(fields) >= 2:
				if i == 0 and (fields[0] != 'id' or fields[1] != 'name'):
						raise Exception("Header format Invalid")
				else:
					building_id = False
					try:
						building_id = int(fields[0])
					except:
						format_error += 1

					if building_id:
						obj, created = Building.objects.get_or_create(building_id=building_id, name=fields[1])
						if created:
							new += 1
						else:
							existing += 1
				i += 1
			else:
				format_error += 1

		return Response({'success': True, 'new': new, 'existing': existing, 'format_error': format_error})

class MetersViewSet(viewsets.ModelViewSet):
	model = Meters
	queryset = Meters.objects.all()

	def get_serializer_class(self):
		if self.request.GET.get('meter_id'):
			return DetailMetersSerializer

		return MetersSerializer

	def get_queryset(self):
		qs = super().get_queryset()
		meter_id = self.request.GET.get('meter_id')

		if meter_id is None:
			return qs

		return Meters.objects.filter(meter_id=meter_id)

	def create(self, request):
		file = request.FILES["file"]
		file_data = file.read().decode("utf-8")
		lines = file_data.split("\n")
		i = 0
		new = 0
		existing = 0
		format_error = 0
		wrong_building = 0
		for line in lines:
			fields = line.split(",")
			
			if len(fields) >= 4:
				if i == 0 and (fields[0] != 'building_id' or fields[1] != 'id' or fields[2] != 'fuel' or 'unit' not in fields[3]):
					raise Exception("Header format Invalid")
				else:
					building_id = False
					meter_id = False
					try:
						building_id = int(fields[0])
						meter_id = int(fields[1])
					except:
						format_error += 1

					if building_id and meter_id:
						# try:
							building = Building.objects.get(building_id=building_id)
							obj, created = Meters.objects.get_or_create(building=building, meter_id=meter_id, fuel=fields[2])
							if created:
								new += 1
							else:
								existing += 1
						# except:
						# 	wrong_building += 1
				i += 1
			else:
				format_error += 1

		return Response({'success': True, 'new': new, 'existing': existing, 'wrong_building': wrong_building, 'format_error': format_error})

class MetersReadingsViewSet(viewsets.ModelViewSet):
	model = MetersReadings
	serializer_class = MetersReadingsSerializer
	queryset = MetersReadings.objects.all()

	def get_queryset(self):
		qs = super().get_queryset()
		meter = self.request.GET.get('meter_id')

		if meter is None:
			return qs

		return qs.filter(meter__meter_id=meter)		

	def create(self, request):
		file = request.FILES["file"]
		file_data = file.read().decode("utf-8")
		lines = file_data.split("\n")
		i = 0
		new = 0
		existing = 0
		format_error = 0
		wrong_meter = 0
		meters = {}
		objects = list()
		for line in lines:
			fields = line.split(",")
			
			if len(fields) >= 3:
				if i == 0 and ('consumption' not in fields[0] or 'meter_id' not in fields[1] or 'reading_date_time' not in fields[2]):
					raise Exception("Header format Invalid")
				else:
					meter_id = False
					consumption = False
					reading_date_time = False
					try:
						consumption = float(fields[0])
						meter_id = int(fields[1])
						reading_date_time = parse(fields[2])
					except:
						format_error += 1

					if (consumption or consumption == 0) and meter_id and reading_date_time:
						try:
							if meter_id not in meters:
								meters[meter_id] = Meters.objects.get(meter_id=meter_id)
							new += 1
							objects.append(MetersReadings(meter=meters[meter_id], consumption=consumption, reading_date_time=reading_date_time))
						except:
							wrong_meter += 1
				i += 1
			else:
				format_error += 1

		batch_size = 100
		total_previous = MetersReadings.objects.count()
		result = MetersReadings.objects.bulk_create(objects, batch_size, ignore_conflicts=True)
		# These two counters variables are not very reliable since bulk_insert can occur at the same time
		added = MetersReadings.objects.count() - total_previous
		existing = new - added 

		return Response({'success': True, 'existing': existing, 'added': added, 'wrong_meter': wrong_meter, 'format_error': format_error})
