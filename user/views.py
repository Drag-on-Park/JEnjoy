from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from .utils import send_verification_email, generate_verification_code
from .models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def user(request):
    return render(request, 'user/user.html')

def login(request):
    ## 이전 url로 돌아가기 추가구현 예정
    # 입력받은 email/password확인
    # jwt 토큰 발급 or 세션 생성
    # 실패 시 적절한 에러 응답 

    # 로깅 INFO 로그인 성공(user_id)
    # WARNING 로그인 실패(잘못된 비밀번호, 없는 계정)
    # ERROR 인증시스템 예외 발생

    return render(request, 'user/login.html')

def register(request):
    # 유효성 검증 - 이메일(아이디) 중복 / 비밀번호 규칙
    # DB 저장(비밀번호 해시)
    # 성공 실패 응답 구조정리

    ## 로깅 INFO 회원가입 성공(USER_ID, email)
    ## WARNING 회원가입 실패(reason: duplicate_email)
    ## ERROR   DB 저장 실패 등 예외상황

    if request.method == 'POST':
        # 이메일
        # 이름
        # 닉네임
        # 핸드폰번호
        # 비밀번호
        # 비밀번호 확인

        # 이메일 불러 와야되는데 어떻게 할건지
        #!!!!!! def verify_email_code(request):검증 후 검증됐다 뭔가를 register로 보내야됨
        email_verified = request.POST.get("email_verified", "false")
        if email_verified != "true":
            return JsonResponse({"error": "이메일 인증이 필요합니다."}, status=400)
        
        email = request.POST.get("verified_email")
        name = request.POST['name']
        nickname = request.POST['nickname']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        photo  = request.FILES.get('photo')

        # 비밀번호 검증
        # photo_url 구현


        user = User.objects.create(
            email=email,
            password=password1,
            nickname=nickname,
            phone_number=phone_number,
            photo_url=photo,
            name=name
        )
        user.save()
        user.set_password(password1)        
        user.save()

        login(request, user)
        return redirect("/")
    else:
        return render(request,'user/register.html' )


def send_verification_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        email = data.get('email')
        if not email:
            return JsonResponse({'success': False, 'error': '이메일을 입력하세요.'})
        
        # 이메일 중복 확인 
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': '이미 사용 중인 이메일입니다.'})
        

        verification_code = generate_verification_code()
        request.session['email_verification_code'] = verification_code
        request.session['email'] = email
        request.session.set_expiry(300) # 5분 후 만료

        send_verification_email(email, verification_code)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': '유효하지 않은 요청입니다.'})

## 이메일로 받은 인증코드 검증 
#!!!!!! 검증 후 검증됐다 뭔가를 register로 보내야됨
def verify_email_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        input_code = data.get('email_verification_code')
        session_code = request.session.get('email_verification_code')
        email = request.session.get('email')

        if not input_code or not session_code:
            return JsonResponse({'success': False, 'error': '코드를 확인 할 수 없습니다.'})
        
        if input_code == session_code:
            del request.session['email_verification_code']  # 검증 후 삭제
            return JsonResponse({'success': True, 'message': f'인증 완료'})
        else:
            return JsonResponse({'success': False, 'error': '인증 코드가 일치하지 않습니다.'})
        
    return JsonResponse({'success': False, 'error': '유효하지 않은 요청입니다.'})