from celery import shared_task
from .models import Dictionary, TodayWord
import random

# 00시 하루 한단어 생성
@shared_task
def generate_daily_words():
    # 랜덤 blank_word 인덱스 
    def random_blank_positions(word_len, num_blanks=2):
        if word_len > 5:
            num_blanks = 3
        num_blanks = min(num_blanks, max(1, word_len // 2))  # 글자 길이에 따라 최대 빈칸 수 제한
        return random.sample(range(word_len), num_blanks)
    # 오늘의 단어
    #!! 랜덤 > 리팩토링예정 max(dictionary.views)
    def random_today_word(level):
        words = list(Dictionary.objects.filter(Lv = f"N{level}"))
        today_words = random.sample(words, 2)

        next_level = level-1
        last_words = list(Dictionary.objects.filter(Lv = f"N{next_level}"))
        today_words += (random.sample(last_words, 1)) 

        return today_words
    
    # 기본 JLPT 레벨(!! 가입 유저별 레벨로 변경예정)
    level = 5  
    # today_words = random.sample(list(Dictionary.objects.filter(Lv=f"N{level}")), 3)
    today_words = random_today_word(level)


    # 기존 단어 비활성화
    TodayWord.objects.update(is_active=0)

    # 새로운 단어 추가
    for idx, one in enumerate(today_words):
        blank_word_positions = random_blank_positions(len(one.word), num_blanks=2)
        if 0 in blank_word_positions:   
            blank_word = one.word[0]
        else:
            blank_word = ""
            for i in blank_word_positions:
                blank_word += one.word[i]

        TodayWord.objects.create(
            dictionary=one,
            today_word=one.word,
            today_pronunciation=one.pronunciation,
            today_meaning=one.meaning,
            priority=idx + 1,
            is_active=1,
            blank_word=blank_word,
            today_Lv=one.Lv
        )
    
    return f"새로운 단어 {len(today_words)}개가 생성됨"
