from rest_framework import serializers
from one_secrets.models import Secret
from django.utils import timezone


class SecretCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ["secret", "expires_at"]

    def validate_expires_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Expiration time must be in the future")
        return value
