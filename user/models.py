from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    level = models.CharField(max_length=10)
    photo_url = models.ImageField()     # !이미지필드 경로추가
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    email = models.EmailField(unique=True)  # 이메일 중복 불가 설정

    @property
    def avatar_url(self):
        import urllib.parse
        seed = urllib.parse.quote(self.username)
        return f"https://api.dicebear.com/6.x/identicon/svg?seed={seed}"

    



# 유저 상세 
class User_Detail(models.Model):
    pass

# 기본 사용자 모델에는 username, password, email, first_name, last_name 등 기본적인 필드들이 포함.
    # username은 식별자
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='custom_user_set',  # related_name 변경
    #     blank=True,
    #     help_text=('The groups this user belongs to. A user will get all permissions '
    #                'granted to each of their groups.'),
    #     verbose_name=('groups'),
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='custom_user_permissions_set',  # related_name 변경
    #     blank=True,
    #     help_text=('Specific permissions for this user.'),
    #     verbose_name=('user permissions'),
    # )
