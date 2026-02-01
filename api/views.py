from django.db import transaction
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SecretCreateSerializer
from one_secrets.models import Secret


class SecretCreateAPIView(APIView):
    def post(self, request):
        """ POST-View:
        Принять JSON → валидация через serializer → создать Secret → вернуть uuid.
        """
        serializer = SecretCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        secret = Secret.objects.create(**serializer.validated_data)

        return Response(
            {"uuid": str(secret.uuid)},
            status=status.HTTP_201_CREATED,
        )


class SecretReadAPIView(APIView):
    def get(self, request, uuid):

        try:  # Получаем объект или возвращаем 404
            with transaction.atomic():
                obj = Secret.objects.select_for_update().get(uuid=uuid)  # Блокирует строку секрета до конца транзакции
                secret_text = obj.read_once()  # Вызываем доменный метод
        except Secret.DoesNotExist:
            raise Http404("Секрет не существует")

        # Возвращаем шаблон с контекстом 410
        if secret_text is None:
            return Response(
                {"detail": "Secret already read or expired"},
                status=status.HTTP_410_GONE,
            )
        else:
            return Response(
                {"secret": secret_text},
                status=status.HTTP_200_OK,
            )
