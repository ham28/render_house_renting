from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('properties/add/', views.addProperty, name='add_property'),
]