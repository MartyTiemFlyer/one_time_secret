import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, datetime
from one_secrets.models import Secret
from api.views import SecretReadAPIView
from rest_framework.test import APIClient


FUTURE = timezone.make_aware(datetime(2099, 1, 1))


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_get_secret_first_time_returns_200(api_client):
    # GIVEN
    secret = Secret.objects.create(secret="Mas", expires_at=FUTURE)
    res = api_client.get(f"/api/secrets/{secret.uuid}/")
    assert res.status_code == 200
    assert res.json()['secret'] == 'Mas'


@pytest.mark.django_db
def test_get_secret_second_time_returns_410(api_client):
    secret = Secret.objects.create(secret="Mas", expires_at=FUTURE)
    res = api_client.get(f"/api/secrets/{secret.uuid}/")
    res = api_client.get(f"/api/secrets/{secret.uuid}/")
    assert res.status_code == 410
    assert res.json()['detail'] == "Secret already read or expired"



@pytest.mark.django_db
def test_get_secret_second_time_returns_410(api_client):
    secret = Secret.objects.create(secret="Mas", expires_at=FUTURE)
    res = api_client.post(url=123456, data=, format='json')
