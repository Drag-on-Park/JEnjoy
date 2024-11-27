from django.urls import path
from . import views

app_name = 'jenmon'
urlpatterns = [
    path('', views.jenmon, name='jenmon'),
]
