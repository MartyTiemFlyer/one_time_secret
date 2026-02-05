from datetime import timedelta

from rest_framework import serializers
from one_secrets.models import Secret
from django.utils import timezone


class SecretCreateSerializer(serializers.ModelSerializer):
    """ModelSerializer - Поля сериализатора = поля модели"""
    class Meta:
        model = Secret
        fields = ["secret", "expires_at"]

    @staticmethod
    def validate_expires_at(value):
        now = timezone.now()
        if value <= now:
            raise serializers.ValidationError("Должно быть в будущем")
        if value > now + timedelta(days=7):
            raise serializers.ValidationError("Максимум 7 дней")
        return value

    def validate(self, data):
        # Если expires_at не указан → ставим 24 часа по умолчанию
        if 'expires_at' not in data or not data['expires_at']:
            data['expires_at'] = timezone.now() + timedelta(hours=24)
        return data
