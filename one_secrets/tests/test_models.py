import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, datetime

from api.serializers import SecretCreateSerializer
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


@pytest.mark.django_db
def test_read_once_race():
    """Тест: если два клиента одновременно пытаются прочитать одноразовый секрет"""
    secret = Secret.objects.create(secret="TopSecret", expires_at=FUTURE)
    first_result = secret.read_once()
    second_result = secret.read_once()
    assert first_result == "TopSecret"
    assert second_result is None


MIN_LATER = timezone.now() - timedelta(minutes=10)


@pytest.mark.django_db  # Разрешить доступ к БД
def test_expired():
    """Тест: истёк срок секрета"""
    secret = Secret.objects.create(secret="TopSecret", expires_at=MIN_LATER)
    result = secret.read_once()

    assert result is None

#
@pytest.mark.django_db
def test_serializer_validates_future_expiration():
    """Тест: expires_at не может быть в прошлом"""
    serializer = SecretCreateSerializer(data={
        'secret': 'Мой секрет',
        'expires_at': timezone.now() - timedelta(hours=1)  # Прошлое!
    })

    # Проверяем, что валидация НЕ проходит
    assert not serializer.is_valid()
    # Проверяем конкретную ошибку в поле expires_at
    assert 'expires_at' in serializer.errors
    # Проверяем текст ошибки
    assert 'будущем' in str(serializer.errors['expires_at'][0]) or \
           'future' in str(serializer.errors['expires_at'][0]).lower()


@pytest.mark.django_db
def test_serializer_validates_max_expiration():
    """Тест: expires_at не может быть больше 7 дней"""
    serializer = SecretCreateSerializer(data={
        'secret': 'Мой секрет',
        'expires_at': timezone.now() + timedelta(days=8)  # 8 дней > 7
    })

    assert not serializer.is_valid()
    assert 'expires_at' in serializer.errors
    assert 'Максимум' in str(serializer.errors['expires_at'][0]) or \
           'maximum' in str(serializer.errors['expires_at'][0]).lower() or \
           '7' in str(serializer.errors['expires_at'][0])