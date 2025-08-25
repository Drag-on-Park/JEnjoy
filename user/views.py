from django.shortcuts import render
import json
from django.http import JsonResponse
from .utils import send_verification_email, generate_verification_code

# Create your views here.
def user(request):
    return render(request, 'user/user.html')

def login(request):
    ## 이전 url로 돌아가기 추가구현 예정
    
    return render(request, 'user/login.html')

def register(request):
    return render(request,'user/register.html' )

def send_verification_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'error': '이메일을 입력하세요.'})

        verification_code = generate_verification_code()
        request.session['email_verification_code'] = verification_code
        request.session['email'] = email
        send_verification_email(email, verification_code)
        
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': '유효하지 않은 요청입니다.'})