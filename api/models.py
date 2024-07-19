"""
Models
"""
from django.db import models
from django.contrib.auth.models import User


class UserPreference(models.Model):
    """
    User preference model
    Args:
        models (_type_): 
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_city = models.CharField(max_length=100, blank=True)
    temperature_unit = models.CharField(
        max_length=1, choices=[('C', 'Celsius'), ('F', 'Fahrenheit')], default='C')
    objects = models.Manager()

class WeatherData(models.Model):
    """
    Weather data model
    Args:
        models (_type_): 
    """
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    condition = models.CharField(max_length=100)
    date = models.DateField()
    objects = models.Manager()
