import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, datetime

from one_secrets.models import Secret

FUTURE = timezone.make_aware(datetime(2099, 1, 1))


@pytest.mark.django_db  # Разрешить доступ к БД
def test_read_first():
    secret = Secret.objects.create(secret="Mas", expires_at=FUTURE)
    res = secret.read_once()
    assert res == "Mas"


@pytest.mark.django_db
def test_read_once_returns_none_on_second_call():
    secret = Secret.objects.create(secret="Masa", expires_at=FUTURE)

    res = secret.read_once()
    res = secret.read_once()
    assert res is None
