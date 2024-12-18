# DB파일 dump
from django.core.management.base import BaseCommand
from dictionary.models import Dictionary
import sqlite3

class Command(BaseCommand):
    help = 'Migrate data from old crawling_data.db to the Django Dictionary table'

    def handle(self, *args, **kwargs):
        source_db = '/Users/dragonpark/Desktop/Workspace/crawling/crawling_data.db'

        connection = sqlite3.connect(source_db)
        cursor = connection.cursor()

        # 먼저 컬럼 존재 여부 확인
        cursor.execute("PRAGMA table_info(words)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'views' in columns:
            select_query = 'SELECT word, pronunciation, meaning, audio_path, POS, Lv, COALESCE(views, 0) AS views FROM words'
        else:
            select_query = 'SELECT word, pronunciation, meaning, audio_path, POS, Lv, 0 AS views FROM words'

        cursor.execute(select_query)
        rows = cursor.fetchall()

        for row in rows:
            word, pronunciation, meaning, audio_path, POS, Lv, views = row

            Lv_mapping = {
                1: 'N1',
                2: 'N2',
                3: 'N3',
                4: 'N4',
                5: 'N5'
            }
            Lv_str = Lv_mapping.get(int(Lv), str(Lv))

            Dictionary.objects.create(
                word=word,
                pronunciation=pronunciation if pronunciation else '',
                meaning=meaning,
                audio_path=audio_path if audio_path else '',
                POS=POS,
                Lv=Lv_str,
                views=views  # 기본값 저장
            )

        connection.close()
        self.stdout.write('Data migration completed successfully.')
