from django.urls import path
from . import views

app_name = 'dictionary'
urlpatterns = [
    path('', views.dictionary, name='dictionary'),
    path('search', views.dictionary_search, name='dictionary_search'),
    path('cross_puzzle', views.crosspuzzle, name='dictionary_cross_puzzle'),
]
