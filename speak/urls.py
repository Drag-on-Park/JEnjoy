from django.urls import path
from . import views

app_name = 'speak'

urlpatterns = [
    path('', views.speak, name='speak'),
]
