from django.urls import path
from . import  views

app_name = 'user'
urlpatterns = [
    path('', views.user, name='user'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),

]
