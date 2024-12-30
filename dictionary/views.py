from django.shortcuts import render
from .models import Dictionary, TodayWord
from django.utils import timezone
import random





# Create your views here.
def dictionary(request):
    # blank_word가 빠진 단어 
    def generate_blank_word(original_word, blank_positions):
        return "".join(" " if idx in blank_positions else char for idx, char in enumerate(original_word))

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
    

    
    ### dictionary views
    dictionary = Dictionary.objects.all()    
    #!! 사용자의 JLPT레벨 추가예정
    level = 5
    # 우선순위 카운트
    cnt = 1

    rendered_words = []
    blank_words = []
    card_data = []

    if request.method == 'POST':

        #!! 00시 날짜가 바뀌면 실행
        today_words = random_today_word(level)

        for one in today_words:
            blank_word_positions = random_blank_positions(len(one.word), num_blanks=2)
            if 0 in blank_word_positions:   
                blank_word = one.word[0]
            else:
                blank_word = ""
                for i in blank_word_positions:
                    blank_word += one.word[i]
            
            rendered_words.append(generate_blank_word(one.word,blank_word_positions))
            blank_words.append(blank_word)

            if one.word:
                today_word = TodayWord.objects.create(
                dictionary= one,
                today_word = one.word,
                today_pronunciation = one.pronunciation,
                today_meaning = one.meaning,
                priority = cnt,
                #!! is_active > 오늘의 단어 설정완료 시 이전 단어 is_active = 0
                is_active = 1,
                # blank_word
                blank_word = blank_word,            
                # POS
                today_Lv = one.Lv
            )
            cnt += 1

    # is_active가 today X 0으로 새로 생성된 today_words는 1로
    #     
    # filter 날짜 >  today_words > 우선순위 >
    today = timezone.now().date()
    today_words = TodayWord.objects.filter(date = today).order_by('priority')
    # get method 일 때 rendered_words, blank_words 불러오기 
    # for idx, obj in enumerate(today_words):
    #     blank_words.append(obj.blank_word)
    #     blank_word_positions = [obj.today_word.find(today_words[idx].blank_word)]

    #     # idx for idx, char in enumerate(obj.today_word) if char in obj.blank_word
    

    #     rendered_words.append(generate_blank_word(obj.today_word,blank_word_positions))

        # 카드 데이터 생성
    for idx, obj in enumerate(today_words):
        blank_word_positions = [obj.today_word.find(char) for char in obj.blank_word]
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
    # 12시 > 오늘의 단어 db 저장

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
        result_query = Dictionary.objects.filter(meaning__contains = search_word)
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



