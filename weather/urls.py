from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('home_fahrenheit/', views.home_fahrenheit, name='home_fahrenheit'),
    path('home_detalle/', views.home_detalle, name='home_detalle'),
]