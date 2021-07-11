from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_ead, name='index_ead'),
]