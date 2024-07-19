'''
Api functions
'''

from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import UserPreference, WeatherData
from .serializers import UserSerializer, UserPreferenceSerializer, WeatherDataSerializer
from .utils import get_weather_data


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print("Received login request:", request.data)  # Debug print
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            print("Login successful")
        else:
            print("Login failed:", response.data)
        return response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow anyone to register


def debug_view(request):
    print("Debug view hit!")
    return HttpResponse("Debug view")

class UserPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print("get_queryset called")
        return UserPreference.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        print("list method called")
        queryset = self.get_queryset()
        if not queryset.exists():
            print("Creating default preferences")
            UserPreference.objects.create(user=request.user, default_city='', temperature_unit='C')
            queryset = self.get_queryset()

        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print("create method called")
        existing_preferences = self.get_queryset().first()
        if existing_preferences:
            serializer = self.get_serializer(existing_preferences, data=request.data, partial=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_preferences(request):
    if request.method == 'GET':
        try:
            preference = UserPreference.objects.get(user=request.user)
            serializer = UserPreferenceSerializer(preference)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        serializer = UserPreferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_weather(request):
    city = request.query_params.get('city', 'London')
    data = get_weather_data('weather', {'q': city})

    if data:
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
        }
        return Response(weather)
    else:
        return Response({'error': 'Unable to fetch weather data'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def forecast(request):
    print("search_weather view called")  # Debug print
    city = request.query_params.get('city', '')
    print(f"Searching for city: {city}")  # Debug print
    data = get_weather_data('forecast', {'q': city})

    if data and 'list' in data:
        forecast_list = []
        current_date = datetime.now().date()
        for i in range(5):  # Get forecast for next 5 days
            day_data = next((item for item in data['list'] if datetime.fromisoformat(
                item['dt_txt']).date() == current_date), None)
            if day_data:
                forecast_list.append({
                    'date': current_date.isoformat(),
                    'temperature': day_data['main']['temp'],
                    'condition': day_data['weather'][0]['main'],
                    'description': day_data['weather'][0]['description'],
                    'icon': day_data['weather'][0]['icon'],
                })
            current_date += timedelta(days=1)
        return Response(forecast_list)
    else:
        return Response({'error': 'Unable to fetch forecast data'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_weather(request):
    print("search_weather view called with params: {request.query_params}")  # Debug print
    city = request.query_params.get('city', '')
    print(f"Searching for city: {city}")  # Debug print
    if not city:
        return Response({'error': 'City parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    data = get_weather_data('weather', {'q': city})

    if data:
        weather = {
            'city': data.get('name', 'Unknown'),
            'temperature': data.get('main', {}).get('temp'),
            'condition': data.get('weather', [{}])[0].get('main', 'Unknown'),
            'description': data.get('weather', [{}])[0].get('description', ''),
            'humidity': data.get('main', {}).get('humidity'),
            'wind_speed': data.get('wind', {}).get('speed'),
            'icon': data.get('weather', [{}])[0].get('icon')
        }
        return Response(weather)
    else:
        return Response({'error': 'Unable to fetch weather data for the specified city'}, status=status.HTTP_404_NOT_FOUND)
