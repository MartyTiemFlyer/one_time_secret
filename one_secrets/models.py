import uuid
from django.db import models
from django.utils import timezone


# Доменная модель - код, отвечающий: что можно и что нельзя делать с сущностью
class Secret(models.Model):
    """
    Секрет, который можно прочитать один раз
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    secret = models.TextField()
    expires_at = models.DateTimeField(null=False)
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Secret {self.uuid}"

    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    def read_once(self) -> str | None:
        """
        Возвращает секрет один раз.
        При повторном вызове или истечении TTL — None.
        """
        if self.is_viewed or self.is_expired():
            print("This: is_viewed or is_expired ")
            return None

        value = self.secret
        self.secret = ""
        self.is_viewed = True
        self.save(update_fields=["secret", "is_viewed"])

        return value