"""
Admin Register
"""
from django.contrib import admin
from .models import UserPreference, WeatherData

admin.site.register(UserPreference)
admin.site.register(WeatherData)
