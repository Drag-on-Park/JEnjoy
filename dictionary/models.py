from django.db import models

# Create your models here.
class Dictionary(models.Model):
    word = models.CharField(max_length=100)  # 일본어 단어
    pronunciation = models.CharField(max_length=100)
    meaning = models.TextField()  # 단어의 뜻
    audio_path = models.CharField(max_length=255)  # 발음 오디오 경로
    POS = models.CharField(max_length=50)  # 품사 (Noun, Verb 등)
    Lv = models.CharField(max_length=2, choices=[
        ('1', 'N1'), ('2', 'N2'), ('3', 'N3'), ('4', 'N4'), ('5', 'N5')
    ])
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.word

