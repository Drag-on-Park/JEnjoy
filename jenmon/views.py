from django.shortcuts import render

# Create your views here.
def jenmon(request):
    return render(request, 'jenmon/jenmon.html')
