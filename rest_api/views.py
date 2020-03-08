from django.shortcuts import render
import csv
import json
import logging

from dateutil.parser import parse
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from itertools import islice

from .models import Building, Meters, MetersReadings
from .serializers import BuildingSerializer, MetersSerializer, MetersReadingsSerializer

class BuildingViewSet(viewsets.ModelViewSet):
	model = Building
	serializer_class = BuildingSerializer
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
	serializer_class = MetersSerializer
	queryset = Meters.objects.all()

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
		wrong_building = 0
		for line in lines:
			fields = line.split(",")
			
			if len(fields) >= 4:
				logging.warning(fields)
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
						try:
							building = Building.objects.get(building_id=building_id)
							obj, created = Meters.objects.get_or_create(building=building, meter_id=meter_id, fuel=fields[2])
							if created:
								new += 1
							else:
								existing += 1
						except:
							wrong_building += 1
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
						meter_id = int(fields[1])
						consumption = float(fields[0])
						reading_date_time = parse(fields[2])
					except:
						format_error += 1

					if meter_id and consumption and reading_date_time:
						# try:
							if meter_id not in meters:
								meters[meter_id] = Meters.objects.get(meter_id=meter_id)
							# if created:
							# 	new += 1
							# 	objects.append(MetersReadings(meter=meters[meter_id], consumption=consumption, reading_date_time=reading_date_time))
							# else:
							# 	existing += 1

							new += 1
							objects.append(MetersReadings(meter=meters[meter_id], consumption=consumption, reading_date_time=reading_date_time))
						# except:
						# 	wrong_meter += 1
				i += 1

				if i % 1000 == 0:
					logging.warning({'new': new, 'wrong_meter': wrong_meter, 'format_error': format_error})
			else:
				format_error += 1

		batch_size = 100
		total = len(objects)
		i = 0
		sliceObj = slice(0, 99, 100)
		while True:
			batch = list(islice(objects, batch_size))
			logging.warning('%s objects proccessed from %s total', i * batch_size, total)
			logging.warning(batch[0].__dict__)
			if i * batch_size > total:
				break
			# MetersReadings.objects.bulk_create(batch, batch_size)
			i += 1

		return Response({'success': True, 'new': new, 'existing': existing, 'wrong_meter': wrong_meter, 'format_error': format_error})
