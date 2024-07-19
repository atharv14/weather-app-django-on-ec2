"""    
Serializers
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPreference, WeatherData


class UserSerializer(serializers.ModelSerializer):
    """

    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """
    class Meta:
        """
        Meta
        """
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserPreferenceSerializer(serializers.ModelSerializer):
    """

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        """
        Meta
        """
        model = UserPreference
        fields = ['default_city', 'temperature_unit']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        return UserPreference.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.default_city = validated_data.get(
            'default_city', instance.default_city)
        instance.temperature_unit = validated_data.get(
            'temperature_unit', instance.temperature_unit)
        instance.save()
        return instance


class WeatherDataSerializer(serializers.ModelSerializer):
    """

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        """
        Meta
        """
        model = WeatherData
        fields = '__alL__'
