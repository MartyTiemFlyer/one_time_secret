from django.urls import path
from .views import SecretCreateAPIView, SecretReadAPIView

# api_urls.py
urlpatterns = [
    path("secrets/", SecretCreateAPIView.as_view(), name="secret-create"),
    path("secrets/<uuid:uuid>/", SecretReadAPIView.as_view(), name="secret-read"),

]
