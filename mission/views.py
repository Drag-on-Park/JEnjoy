from django.shortcuts import render
from dictionary.models import Dictionary
# Create your views here.
def mission(request):
    return render(request,'mission/mission.html')

def jentype(request):
    
    return render(request,'mission/jentype.html')
