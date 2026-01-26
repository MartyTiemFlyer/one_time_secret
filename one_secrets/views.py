from django.shortcuts import render

# view - получает запрос, обращается к модели, возвращает ответ
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseGone
from one_secrets.models import Secret


def object_detail(request, uuid):
    # Получаем объект или возвращаем 404
    obj = get_object_or_404(Secret, uuid=uuid)

    # Вызываем доменный метод (например, read_once)
    secret_text = obj.read_once()

    # Возвращаем шаблон с контекстом
    if secret_text is None:
        return HttpResponseGone("Секрет уничтожен или не существует")
    else:
        return render(request, 'secret_detail.html', {'secret_text': secret_text})