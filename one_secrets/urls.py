from django.urls import path
from . import views

# URL list, связывает адрес в браузере с функцией/классом view

#secret_url
urlpatterns = [
    path('<uuid:uuid>/', views.object_detail, name='object_detail'),
]
