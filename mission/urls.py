from django.urls import path
from . import views

app_name = 'mission'
urlpatterns = [
    path('', views.mission, name='mission'),
    path('typing_practice/', views.typing_practice, name='typing_practice'),
]
