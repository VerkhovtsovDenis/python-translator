from . import views
from django.urls import include, path

urlpatterns = [
    # Главная страница.
    path('', views.index),
]
