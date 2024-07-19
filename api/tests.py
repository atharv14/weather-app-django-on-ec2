"""
Test Cases
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserPreference


class WeatherAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_current_weather(self):
        response = self.client.get('/api/current-weather/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('temperature', response.data) # type: ignore
        self.assertIn('condition', response.data) # type: ignore

    def test_forecast(self):
        response = self.client.get('/api/forecast/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5) # type: ignore

    def test_search_weather(self):
        response = self.client.get('/api/search-weather/', {'city': 'London'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], 'London') # type: ignore

    def test_user_preference(self):
        data = {'default_city': 'Paris', 'temperature_unit': 'C'}
        response = self.client.post('/api/preferences/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserPreference.objects.count(), 1)
        self.assertEqual(UserPreference.objects.get().default_city, 'Paris')
