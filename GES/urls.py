from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_ges, name='index_ges'),
]