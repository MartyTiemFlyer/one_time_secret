from django.shortcuts import render

# view - получает запрос, обращается к модели, возвращает ответ
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseGone, Http404
from one_secrets.models import Secret
from django.db import transaction


def object_detail(request, uuid):
    """
    Return one-time secret.

    Reads and invalidates the secret in a single transaction.
    Raises 404 if not found, returns 410 if already destroyed.
    """
    try:                                    # Получаем объект или возвращаем 404
        with transaction.atomic():
            obj = Secret.objects.select_for_update().get(uuid=uuid)  # Блокирует строку секрета до конца транзакции
            secret_text = obj.read_once()   # Вызываем доменный метод
    except Secret.DoesNotExist:
        raise Http404("Секрет не существует")

    # Возвращаем шаблон с контекстом 410
    if secret_text is None:
        return HttpResponseGone("Секрет уничтожен или не существует")
    else:
        return render(request, 'secret_detail.html', {'secret_text': secret_text})