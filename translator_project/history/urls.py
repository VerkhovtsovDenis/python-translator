from . import views
from django.urls import include, path

app_name = 'history'

urlpatterns = [
    # Главная страница.
    path('', views.index, name='index'),
]
