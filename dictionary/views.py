from django.shortcuts import render
from .models import Dictionary, TodayWord, Puzzle, PuzzleWord
from django.utils import timezone
import random
from django.db.models import Q

# Create your views here.
def dictionary(request):
    # blank_word가 빠진 단어 
    def generate_blank_word(original_word, blank_positions):
        return "".join(" " if idx in blank_positions else char for idx, char in enumerate(original_word))

    card_data = []

    # is_active가 today X 0으로 새로 생성된 today_words는 1로
    # filter 날짜 >  today_words > 우선순위 >
    today = timezone.now().date()
    today_words = TodayWord.objects.filter(date = today).order_by('priority')
    # get method 일 때 rendered_words, blank_words 불러오기 

    # 카드 데이터 생성
    for idx, obj in enumerate(today_words):
        
        # blank_word_positions = [obj.today_word.find(char) for char in obj.blank_word]
        blank_word_positions = [i for i, char in enumerate(obj.today_word) if char in obj.blank_word]

        rendered_word = generate_blank_word(obj.today_word, blank_word_positions)

        card_data.append({
            'today_word': obj.today_word,
            'rendered_word': rendered_word,
            'blank_word': obj.blank_word,
            'today_pronunciation': obj.today_pronunciation,
            'today_meaning': obj.today_meaning,
            'today_Lv': obj.today_Lv,
            'today_POS': obj.dictionary.POS if hasattr(obj.dictionary, 'POS') else '',
        })

    context = {
        'card_data': card_data
    }
    return render(request, 'dictionary/dictionary.html', context)

def dictionary_search(request):
    # search word == 일본어 로직
    # search 들어온 값 확인 후 맞게 설계
    if request.method == 'POST':
        search_word = request.POST.get('search_query')
        # 중간 로직 필요 일본어 한국어 모두 검색 기능 
        result_query = Dictionary.objects.filter(
            Q(word__icontains=search_word) |
            Q(pronunciation__icontains=search_word) |
            Q(meaning__icontains=search_word))
        context = {
            'search_word' : search_word,
            'search_result' : result_query
        }

        
    # 기본 context 초기화
    # context = {
    #     'search_form': PostSearchForm(),
    #     'search_term': '',
    #     'object_list': None,
    #     'paginator': None,
    #     'page_obj': None,
    # }
    
    # search_term = request.GET.get('search_word', '')
    
    # if request.method == "POST":
    #     search_form = PostSearchForm(request.POST)
    #     if search_form.is_valid():
    #         search_term = search_form.cleaned_data['search_word']
    #         post_list = Post.objects.filter(
    #             Q(post_title__icontains=search_term) | 
    #             Q(post_content__icontains=search_term)
    #         ).distinct()
    #     else:
    #         post_list = Post.objects.none()
    #         context.update({
    #             'search_form': search_form,
    #             'form_errors': search_form.errors
    #         })
    # else:
    #     # GET 요청에서 검색어로 게시물 필터링
    #     if search_term:
    #         post_list = Post.objects.filter(
    #             Q(post_title__icontains=search_term) | 
    #             Q(post_content__icontains=search_term)
    #         ).distinct()
    #     else:
    #         post_list = Post.objects.none()
    
    # # 페이지네이션
    # paginator = Paginator(post_list, 12)
    # page_number = request.GET.get('page', 1)
    # page_obj = paginator.get_page(page_number)

    # # context 업데이트
    # context.update({
    #     'search_term': search_term,
    #     'object_list': page_obj,
    #     'paginator': paginator,
    #     'page_obj': page_obj,
    # })
        
        return render(request, 'dictionary/dictionary_search.html', context)
    else:
        return render(request, 'dictionary/dictionary_search.html')

# def crosspuzzle(request):
#     # 오늘 날짜의 퍼즐 확인
#     today = timezone.now().date()
#     puzzle = Puzzle.objects.filter(date=today).first()

#     if not puzzle:
#         grid = [['' for _ in range(12)] for _ in range(12)]
#         puzzle_words = []

#         # 첫 단어 배치
#         first_word = random.choice(
#             Dictionary.objects.filter(word__regex=r'^.{2,8}$')  # 2~8자
#         )
#         x, y = random.randint(0, 3), random.randint(0, 2)
#         if not place_word(grid, first_word.word, x, y, 'across'):
#             raise ValueError("첫 단어 배치 실패")
#         puzzle_words.append({
#             'word': first_word,
#             'x': x,
#             'y': y,
#             'direction': 'across',
#             'clue': f"{first_word.meaning} {first_word.POS} JLPT N{first_word.Lv}"
#         })

#         # 단어 배치 루프
#         target_words = random.randint(14, 20)  # 가로+세로 7~10개씩
#         placed_words = [first_word.word]
#         attempts = 0
#         max_attempts = 100  # 무한 루프 방지

#         while len(puzzle_words) < target_words and attempts < max_attempts:
#             attempts += 1
#             # 랜덤 단어 선택 (2~8자)
#             candidate = random.choice(
#                 Dictionary.objects.filter(word__regex=r'^.{2,8}$')
#             )
#             if candidate.word in placed_words:
#                 continue

#             # 기존 단어와 교차 시도
#             placed_success = False
#             for placed in puzzle_words:
#                 intersection = find_intersection(placed['word'].word, candidate.word)
#                 if intersection:
#                     placed_idx, candidate_idx = intersection
#                     if placed['direction'] == 'across':
#                         # 기존 단어가 가로 -> 새 단어는 세로
#                         x = placed['x'] + placed_idx
#                         y = placed['y'] - candidate_idx
#                         direction = 'down'
#                     else:
#                         # 기존 단어가 세로 -> 새 단어는 가로
#                         x = placed['x'] - candidate_idx
#                         y = placed['y'] + placed_idx
#                         direction = 'across'

#                     # 배치 가능 여부 확인 및 배치
#                     if x >= 0 and y >= 0 and place_word(grid, candidate.word, x, y, direction):
#                         puzzle_words.append({
#                             'word': candidate,
#                             'x': x,
#                             'y': y,
#                             'direction': direction,
#                             'clue': f"{candidate.meaning} {candidate.POS} JLPT N{candidate.Lv}"
#                         })
#                         placed_words.append(candidate.word)
#                         placed_success = True
#                         break
#             if placed_success:
#                 continue

#             # 교차 실패 시 새 위치에 배치 시도
#             direction = random.choice(['across', 'down'])
#             for _ in range(10):  # 최대 10번 시도
#                 if direction == 'across':
#                     x = random.randint(0, 11 - len(candidate.word))
#                     y = random.randint(0, 11)
#                 else:
#                     x = random.randint(0, 11)
#                     y = random.randint(0, 11 - len(candidate.word))
#                 if place_word(grid, candidate.word, x, y, direction):
#                     puzzle_words.append({
#                         'word': candidate,
#                         'x': x,
#                         'y': y,
#                         'direction': direction,
#                         'clue': f"{candidate.meaning} {candidate.POS} JLPT N{candidate.Lv}"
#                     })
#                     placed_words.append(candidate.word)
#                     break

#         # 퍼즐 저장
#         puzzle = Puzzle.objects.create(grid=grid)
#         for pw in puzzle_words:
#             PuzzleWord.objects.create(
#                 puzzle=puzzle,
#                 dictionary_entry=pw['word'],
#                 clue=pw['clue'],
#                 direction=pw['direction'],
#                 start_x=pw['x'],
#                 start_y=pw['y']
#             )

#     # 렌더링 데이터 준비
#     grid = puzzle.grid
#     across_clues = puzzle.words.filter(direction='across').order_by('start_y', 'start_x')
#     down_clues = puzzle.words.filter(direction='down').order_by('start_x', 'start_y')

#     # 번호 부여
#     number_map = {}
#     current_number = 1
#     for word in sorted(puzzle.words.all(), key=lambda w: (w.start_y, w.start_x)):
#         key = (word.start_y, word.start_x)
#         if key not in number_map:
#             number_map[key] = current_number
#             current_number += 1

#     return render(request, 'crosspuzzle.html', {
#         'grid': grid,
#         'across_clues': across_clues,
#         'down_clues': down_clues,
#         'number_map': number_map
#     })


# ##########################
def print_grid(grid):
    """12x12 그리드를 보기 좋게 출력"""
    print("\n    " + " ".join(f"{i:>2}" for i in range(12)))
    print("   +" + "---" * 12 + "+")

    for i, row in enumerate(grid):
        row_str = " ".join(cell if cell else "・" for cell in row)
        print(f"{i:>2} | {row_str} |")

    print("   +" + "---" * 12 + "+\n")

def can_place_word(grid, word, x, y, direction, is_intersection=False):
    """
    교차 퍼즐용 단어 배치 가능성 검사 (더 유연한 교차 허용)
    grid: 12x12 퍼즐 그리드
    word: 단어 문자열
    x, y: 시작 위치
    direction: 'across' or 'down'
    is_intersection: 교차 단어인지 여부
    """
    len_w = len(word)
    
    # 그리드 범위 벗어남 방지
    if direction == 'across':
        if x < 0 or x + len_w > 12 or y < 0 or y >= 12:
            return False
    elif direction == 'down':
        if y < 0 or y + len_w > 12 or x < 0 or x >= 12:
            return False

    intersect_count = 0

    for i, char in enumerate(word):
        cx = x + i if direction == 'across' else x
        cy = y if direction == 'across' else y + i
        cell = grid[cy][cx]

        if cell != '' and cell != char:
            return False  # 다른 글자가 이미 있음
        if cell == char:
            intersect_count += 1

        # 주변 셀 체크 (단어 앞뒤 제외)
        if direction == 'across':
            if cy > 0 and grid[cy - 1][cx] != '':
                return False
            if cy < 11 and grid[cy + 1][cx] != '':
                return False
        else:
            if cx > 0 and grid[cy][cx - 1] != '':
                return False
            if cx < 11 and grid[cy][cx + 1] != '':
                return False

    # 단어 양 끝 체크 (연결 방지)
    if direction == 'across':
        if x > 0 and grid[y][x - 1] != '':
            return False
        if x + len_w < 12 and grid[y][x + len_w] != '':
            return False
    else:
        if y > 0 and grid[y - 1][x] != '':
            return False
        if y + len_w < 12 and grid[y + len_w][x] != '':
            return False

    # 교차 단어라면 실제 교차가 1개 이상 있어야 인정
    if is_intersection and intersect_count == 0:
        return False

    return True

def place_word(grid, word, x, y, direction, is_intersection=False):
    if not can_place_word(grid, word, x, y, direction, is_intersection):
        return False

    for i, char in enumerate(word):
        cx = x + i if direction == 'across' else x
        cy = y if direction == 'across' else y + i
        grid[cy][cx] = char

    return True

def find_intersections(word1, word2):
    """두 단어의 모든 교차 지점 찾기"""
    intersections = []
    for i, c1 in enumerate(word1):
        for j, c2 in enumerate(word2):
            if c1 == c2:
                intersections.append((i,j))
    return intersections

def find_cross_candidate(char):
    """교차 가능한 단어 검색"""
    candidates = Dictionary.objects.filter(word__contains=char, word__regex=r'^.{2,8}$')
    print(f"Candidates for '{char}': {[c.word for c in candidates]}")
    return candidates


def crosspuzzle(request):
    today = timezone.localdate()
    puzzle = Puzzle.objects.filter(date=today).first()

    if not puzzle:
        grid = [['' for _ in range(12)] for _ in range(12)]
        puzzle_words = []

        # 첫 단어 배치
        first_word = random.choice(Dictionary.objects.filter(word__regex=r'^.{3,8}$'))
        x, y = random.randint(0, 3), random.randint(0, 2)
        if not place_word(grid, first_word.word, x, y, 'across'):
            raise ValueError("첫 단어 배치 실패")

        puzzle_words.append({
            'word': first_word,
            'x': x,
            'y': y,
            'direction': 'across',
            'clue': f"{first_word.meaning} {first_word.POS} JLPT {first_word.Lv}"
        })

        target_words = random.randint(10, 14)
        placed_words = [first_word.word]
        attempts = 0
        max_attempts = 2000
        across_count = 1
        down_count = 0
        target_across = target_words // 2
        target_down = target_words - target_across

        while len(puzzle_words) < target_words and attempts < max_attempts:
            attempts += 1

            if across_count < target_across:
                direction = 'across'
            elif down_count < target_down:
                direction = 'down'
            else:
                direction = random.choice(['across', 'down'])

            placed_success = False
            random.shuffle(puzzle_words)

            for placed in puzzle_words:
                for char in placed['word'].word:
                    candidates = find_cross_candidate(char)
                    if not candidates:
                        continue

                    random.shuffle(candidates)
                    for candidate in candidates:
                        if candidate.word in placed_words:
                            continue

                        intersections = find_intersections(placed['word'].word, candidate.word)
                        random.shuffle(intersections)

                        for placed_idx, candidate_idx in intersections:
                            if placed['direction'] == 'across':
                                x = placed['x'] + placed_idx
                                y = placed['y'] - candidate_idx
                                new_dir = 'down'
                            else:
                                x = placed['x'] - candidate_idx
                                y = placed['y'] + placed_idx
                                new_dir = 'across'

                            if new_dir == 'across':
                                if x < 0 or x + len(candidate.word) > 12 or y < 0 or y >= 12:
                                    continue
                            else:
                                if y < 0 or y + len(candidate.word) > 12 or x < 0 or x >= 12:
                                    continue

                            if can_place_word(grid, candidate.word, x, y, new_dir, is_intersection=True):
                                if place_word(grid, candidate.word, x, y, new_dir, is_intersection=True):
                                    puzzle_words.append({
                                        'word': candidate,
                                        'x': x,
                                        'y': y,
                                        'direction': new_dir,
                                        'clue': f"{candidate.meaning} {candidate.POS} JLPT {candidate.Lv}"
                                    })
                                    placed_words.append(candidate.word)
                                    if new_dir == 'across':
                                        across_count += 1
                                    else:
                                        down_count += 1
                                    placed_success = True
                                    break
                        if placed_success:
                            break
                    if placed_success:
                        break
                if placed_success:
                    break

            if not placed_success:
                new_word = random.choice(Dictionary.objects.filter(word__regex=r'^.{3,8}$'))
                if new_word.word in placed_words:
                    continue

                for _ in range(20):
                    rand_x = random.randint(0, 11)
                    rand_y = random.randint(0, 11)
                    rand_dir = random.choice(['across', 'down'])

                    if can_place_word(grid, new_word.word, rand_x, rand_y, rand_dir):
                        place_word(grid, new_word.word, rand_x, rand_y, rand_dir)
                        puzzle_words.append({
                            'word': new_word,
                            'x': rand_x,
                            'y': rand_y,
                            'direction': rand_dir,
                            'clue': f"{new_word.meaning} {new_word.POS} JLPT {new_word.Lv}"
                        })
                        placed_words.append(new_word.word)
                        if rand_dir == 'across':
                            across_count += 1
                        else:
                            down_count += 1
                        break

        puzzle = Puzzle.objects.create(grid=grid)
        for pw in puzzle_words:
            PuzzleWord.objects.create(
                puzzle=puzzle,
                dictionary_entry=pw['word'],
                clue=pw['clue'],
                direction=pw['direction'],
                start_x=pw['x'],
                start_y=pw['y']
            )

    grid = puzzle.grid
    across_clues = puzzle.words.filter(direction='across').order_by('start_y', 'start_x')
    down_clues = puzzle.words.filter(direction='down').order_by('start_x', 'start_y')

    number_map = {}
    current_number = 1
    for word in sorted(puzzle.words.all(), key=lambda w: (w.start_y, w.start_x)):
        key = (word.start_y, word.start_x)
        if key not in number_map:
            number_map[key] = current_number
            current_number += 1

    return render(request, 'crosspuzzle.html', {
        'grid': grid,
        'across_clues': across_clues,
        'down_clues': down_clues,
        'number_map': number_map
    })
