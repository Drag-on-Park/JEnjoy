from django.db import models

# Create your models here.
class Dictionary(models.Model):
    word = models.CharField(max_length=100)  # 일본어 단어
    pronunciation = models.CharField(max_length=100)
    romaji = models.CharField(max_length=100,null=True,blank=True) # pronunciation >> 로마표기
    meaning = models.TextField()  # 단어의 뜻
    audio_path = models.CharField(max_length=255)  # 발음 오디오 경로
    POS = models.CharField(max_length=50)  # 품사
    Lv = models.CharField(max_length=2, choices=[
        ('1', 'N1'), ('2', 'N2'), ('3', 'N3'), ('4', 'N4'), ('5', 'N5')
    ])
    views = models.IntegerField(default=0)
    

    def __str__(self):
        return self.word

# 레벨별 

# 단어선택 기준
# 블랭크 기준
# 사전에 단어가 삭제 됐을 때  연쇄 삭제? 남겨놓는가 
# 삭제 된다면 다른 단어로 대체 
# 스냅샷 
# blank_word 추가예정
class TodayWord(models.Model):
    date = models.DateField(auto_now_add=True)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.SET_NULL, null=True)
    today_word = models.CharField(max_length=100)
    today_pronunciation = models.CharField(max_length=100, null=True, blank=True)
    today_meaning = models.TextField(null=True, blank=True)
    today_POS = models.CharField(max_length=50, null=True) 
    today_Lv = models.CharField(max_length=2, choices=[
        ('1', 'N1'), ('2', 'N2'), ('3', 'N3'), ('4', 'N4'), ('5', 'N5')
    ], null=True)
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    blank_word = models.CharField(max_length=50, null=True)

    def save(self, *args, **kwargs):
        if self.dictionary:
            self.today_word = self.dictionary.word
            self.today_pronunciation = self.dictionary.pronunciation
            self.today_meaning = self.dictionary.meaning
            self.today_POS = self.dictionary.POS
            self.today_Lv = self.dictionary.Lv
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.date} - {self.today_word}"

class Puzzle(models.Model):
    date = models.DateField(auto_now_add=True)  # 생성 날짜
    grid = models.JSONField(null=True, blank=True)  # 퍼즐 12x12 그리드 저장 (optional, 렌더링 용도)

class PuzzleWord(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='words')
    dictionary_entry = models.ForeignKey(Dictionary, on_delete=models.SET_NULL, null=True)
    clue = models.TextField() # !! 설명 
    direction = models.CharField(max_length=10, choices=[('across', '가로'), ('down', '세로')])
    start_x = models.IntegerField()
    start_y = models.IntegerField()


# example_sentence 사용자 참여 예문
