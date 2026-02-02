# view - получает запрос, обращается к модели, возвращает ответ

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseGone, Http404
from one_secrets.models import Secret
from django.db import transaction


def index(request):
    return render(request, "one_secrets/index.html")


def secret_page(request, uuid):
    return render(request, "one_secrets/secret_detail.html", {"uuid": uuid})
