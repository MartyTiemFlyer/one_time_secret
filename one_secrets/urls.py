from django.urls import path
from . import views

# URL list, связывает адрес в браузере с функцией/классом view

#secret_url
urlpatterns = [
    path("secret/<uuid:uuid>/", views.secret_page, name="secret_page"),

]
