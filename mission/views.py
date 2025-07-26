from django.shortcuts import render

# Create your views here.
def mission(request):
    return render(request,'mission/mission.html')

def typing_practice(request):
    return render(request,'mission/typing_practice.html')
