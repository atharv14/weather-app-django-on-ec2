'''
URL API path
'''

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'preferences', views.UserPreferenceViewSet,
                basename='preference')
router.register(r'weather-data', views.WeatherDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('debug/', views.debug_view, name='debug'),
    path('current-weather/', views.current_weather, name='current_weather'),
    path('forecast/', views.forecast, name='forecast'),
    path('search-weather/', views.search_weather, name='search_weather'),
    # path('preferences/', views.UserPreferenceViewSet.as_view(
    #     {'get': 'list', 'post': 'create'}), name='user_preferences'),
    # path('preferences/<int:pk>/', views.UserPreferenceViewSet.as_view(
    #     {'put': 'update', 'patch': 'partial_update'}), name='user_preferences_detail'),
]
