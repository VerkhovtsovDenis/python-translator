from . import views
from django.urls import include, path

app_name = 'main'

urlpatterns = [
    # Главная страница.
    path('', views.index, name='index'),
	path('about/', views.about, name='about'),

]
