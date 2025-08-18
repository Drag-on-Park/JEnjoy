# accounts/adapters.py
from allauth.account.utils import user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        # Google, Facebook 등에서 내려주는 이름 처리
        first_name = data.get('first_name', '') or ''
        last_name = data.get('last_name', '') or ''
        full_name = f"{first_name} {last_name}".strip()

        if not full_name:  # 혹시라도 둘 다 없는 경우
            full_name = data.get('name', '')

        user_field(user, 'name', full_name)  # name 필드에 저장
        return user
