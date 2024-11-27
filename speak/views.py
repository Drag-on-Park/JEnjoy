from django.shortcuts import render

# Create your views here.
def speak(request):
    return render(request, 'speak/speak.html')
