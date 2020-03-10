import logging

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class BuildingsViewTests(APITestCase):
	def test_obtaining_buildings_list(self):
		response = self.client.get(reverse('buildings-list'))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(len(response.data), 0)