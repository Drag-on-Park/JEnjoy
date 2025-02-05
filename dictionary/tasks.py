from celery import shared_task
from .models import Dictionary, TodayWord
import random

@shared_task
def generate_daily_words():
    level = 5  # 기본 JLPT 레벨
    today_words = random.sample(list(Dictionary.objects.filter(Lv=f"N{level}")), 3)

    # 기존 단어 비활성화
    TodayWord.objects.update(is_active=0)

    # 새로운 단어 추가
    for idx, one in enumerate(today_words):
        blank_positions = random.sample(range(len(one.word)), min(2, len(one.word) // 2))
        blank_word = "".join([one.word[i] for i in blank_positions])

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