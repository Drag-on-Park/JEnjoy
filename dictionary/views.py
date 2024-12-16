from django.shortcuts import render
from .models import Dictionary

# Create your views here.
def dictionary(request):
    dictionary = Dictionary.objects.all()
    return render(request, 'dictionary/dictionary.html')
