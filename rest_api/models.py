from django.db import models
from django.utils.translation import gettext as _

class Building(models.Model):
	building_id=models.IntegerField(unique=True)
	name=models.CharField(max_length=100)

	class Meta:
		ordering = ['building_id']

class FuelType(models.IntegerChoices):
	WATER = 1, _('Water')
	GAS = 2, _('Natural Gas')
	ELECTRICITY = 3, _('Electricity')
	__empty__ = _('(Unknown)')

class UnitType(models.IntegerChoices):
	M3 = 1, _('m3')
	KWH = 2, _('kWh')
	__empty__ = _('(Unknown)')

class Meters(models.Model):
	building=models.ForeignKey(Building, on_delete=models.CASCADE, related_name='meters')
	meter_id=models.IntegerField()
	fuel = models.CharField(max_length=20, choices=FuelType.choices)

	class Meta:
		unique_together = ('building', 'meter_id')

class MetersReadings(models.Model):
	meter=models.ForeignKey(Meters, on_delete=models.CASCADE, related_name='readings')
	consumption=models.DecimalField(max_digits=12, decimal_places=4)
	reading_date_time=models.DateTimeField()

	class Meta:
		unique_together = ('meter', 'reading_date_time')
		ordering = ('meter', 'reading_date_time')
