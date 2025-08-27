from django.urls import path
from . import  views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'
urlpatterns = [
    path('', views.user, name='user'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('verify_email_code/', views.verify_email_code, name='verify_email_code'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)