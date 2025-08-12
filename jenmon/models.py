from django.db import models
from user.models import User
from django.conf import settings

# Create your models here.
class Jenmon(models.Model):
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=30) # 속성 불, 물 등
    rarity = models.CharField(max_length=20, default='normal') # 등급 레어, 희귀, 전설 등
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 운영 측 생성일
    updated_at = models.DateTimeField(auto_now=True)      # 운영 측 업데이트일

    def __str__(self):
        return self.name


class UserJenmon(models.Model):
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='jenmons')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jenmons')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jenmons')

    jenmon = models.ForeignKey(Jenmon, on_delete=models.CASCADE, related_name='owned_by_users')
    nickname = models.CharField(max_length=50, blank=True) # 유저가 지은 이름
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    fatigue = models.IntegerField(default=0) # 피로도
    motivation = models.IntegerField(default=100) # 학습 의욕 (0~100)
    # progress = models.FloatField(default=0.0)    # 전체 학습 진척도 (%) / 백엔드에서 로직으로 구현해도됨

    created_at = models.DateTimeField(auto_now_add=True)  # 유저 획득일
    updated_at = models.DateTimeField(auto_now=True)      # 최근 상태 변경일

    def __str__(self):
        return f"{self.user.username}'s {self.nickname or self.jenmon.name}"


# class UserJenmonHistory(models.Model):
#     user_jenmon = models.ForeignKey(UserJenmon, on_delete=models.CASCADE, related_name='history')
#     event_type = models.CharField(max_length=30, choices=[
#         ('create', 'Created'),
#         ('battle', 'Battle'),
#         ('level_up', 'Level Up'),
#         ('evolve', 'Evolve'),
#         ('heal', 'Heal'),
#         ('item_use', 'Item Use'),
#     ])
#     change_detail = models.JSONField()  # 변경 전/후 값 저장
#     reason = models.CharField(max_length=100, blank=True)  # 변경 원인
#     created_at = models.DateTimeField(auto_now_add=True)   # 변경 발생 시점

#     def __str__(self):
#         return f"{self.user_jenmon} - {self.event_type} @ {self.created_at}"
