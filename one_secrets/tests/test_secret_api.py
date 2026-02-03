import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, datetime
from one_secrets.models import Secret
from api.views import SecretReadAPIView
from rest_framework.test import APIClient
from uuid import UUID

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
def test_post_returns_201(api_client):

    payload = {
        "secret": "Mas",
        "expires_at": FUTURE}

    res = api_client.post("/api/secrets/", payload, format="json")

    uuid_str = res.json()["uuid"]

    assert res.status_code == 201
    assert UUID(uuid_str)
    # объект реально появился в базе
    assert Secret.objects.filter(uuid=uuid_str).exists() == True


@pytest.mark.django_db
def test_nevalid_post_returns_400(api_client):
    payload = {
        "secret": 0,
        "expires_at": 0}

    res = api_client.post("/api/secrets/", payload, format="json")

    assert res.status_code == 400
    assert res.json()
    # assert "secret" in res.json()


@pytest.mark.django_db
def test_two_identical_secrets_have_different_uuid(api_client):
    payload = {
        "secret": "Mas",
        "expires_at": FUTURE,
    }

    res1 = api_client.post("/api/secrets/", payload, format="json")
    res2 = api_client.post("/api/secrets/", payload, format="json")

    assert res1.status_code == 201
    assert res2.status_code == 201

    uuid1 = res1.json()["uuid"]
    uuid2 = res2.json()["uuid"]

    # проверяем, что это валидные UUID
    UUID(uuid1)
    UUID(uuid2)

    # и главное — что они разные
    assert uuid1 != uuid2
