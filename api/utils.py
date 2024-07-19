"""
Returns:
    _type_: _description_
"""
import requests
from django.conf import settings


def get_weather_data(endpoint, params):
    url = f"{settings.OPENWEATHERMAP_BASE_URL}/{endpoint}"
    params['appid'] = settings.OPENWEATHERMAP_API_KEY
    params['units'] = 'metric'

    response = requests.get(url, params=params, timeout=10)
    return response.json() if response.status_code == 200 else None
