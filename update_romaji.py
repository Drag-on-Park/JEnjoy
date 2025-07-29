import sqlite3
from pykakasi import kakasi
import os

# 데이터베이스 파일 경로
DB_PATH ='/Users/dragonpark/Desktop/Workspace/JEnjoy/db.sqlite3'

# kakasi 인스턴스 생성 (히라가나/가타카나/한자 -> 로마자) kks = kakasi()
kks = kakasi()
kks.setMode("H", "a")  # Hiragana to ascii
kks.setMode("K", "a")  # Katakana to ascii
kks.setMode("J", "a")  # Japanese characters (Kanji) to  ascii
kks.setMode("r", "Hepburn") # 로마자 표기법 (Hepburn)
conv = kks.getConverter()

def convert_to_romaji(text):
    """일본어 텍스트를 로마자로 변환"""
    return conv.do(text)

def add_romaji_column_and_update():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. 새로운 컬럼 'romaji' 추가 
        # 스크립트에서는 추가 시도를 하지 않거나, 이미  존재하면 무시하도록 처리
        # 만약 아직 모델에만 추가하고 migrate를 안했다면, 먼저 migrate를 실행
        try:
            cursor.execute("ALTER TABLE  dictionary_dictionary ADD COLUMN romaji VARCHAR(100);")
            print("컬럼 'romaji'가 성공적으로  추가되었습니다.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("컬럼 'romaji'가 이미 존재합니다.  업데이트를 진행합니다.")
            else:
                raise e

        # 2. 모든 행을 순회하며 'pronunciation' 또는 'word'  컬럼의 값을 로마자로 변환하여 'romaji'에 업데이트
        # 'word' 컬럼도 함께 조회(한자는 발음 없는 단어있음)
        cursor.execute("SELECT id, pronunciation, word FROM  dictionary_dictionary;")
        rows = cursor.fetchall()

        print(f"총 {len(rows)}개의 튜플을 처리합니다...")
        for row_id, pronunciation, word in rows:
            text_to_convert = ""
            if pronunciation:
                text_to_convert = pronunciation
            elif word: # pronunciation이 비어있으면 word  사용
                text_to_convert = word

            if text_to_convert:
                romaji = convert_to_romaji(text_to_convert)
                cursor.execute(
                    "UPDATE dictionary_dictionary SET romaji = ? WHERE id = ?;",
                    (romaji, row_id)
                )
            else:
                # 변환할 텍스트가 없는 경우 NULL로 설정
                cursor.execute(
                    "UPDATE dictionary_dictionary SET romaji = NULL WHERE id = ?;",
                    (row_id,)
                )
        conn.commit()
        print("모든 튜플의 'romaji' 컬럼 업데이트가  완료되었습니다.")

    except sqlite3.Error as e:
        print(f"데이터베이스 오류 발생: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # pykakasi 라이브러리가 설치되어 있는지 확인
    try:
        import pykakasi
    except ImportError:
        print("pykakasi 라이브러리가 설치되어 있지  않습니다.")
        print("다음 명령어를 실행하여 설치해주세요: pip  install pykakasi")
        exit()

    add_romaji_column_and_update()