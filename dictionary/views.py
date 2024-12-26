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
        num_blanks = min(num_blanks, max(1, word_len // 2))  # 글자 길이에 따라 최대 빈칸 수 제한
        return random.sample(range(word_len), num_blanks)
    
    # 오늘의 단어
    #!! 랜덤 > 리팩토링예정 max(dictionary.views)
    def random_today_word(level):
        words = list(Dictionary.objects.filter(Lv = f"N{level}"))
        today_words = [random.sample(words, 2)]

        next_level = level-1
        last_words = list(Dictionary.objects.filter(Lv = f"N{next_level}"))
        today_words.append(random.sample(last_words, 1)) 

        return today_words
    
    ### dictionary views
    dictionary = Dictionary.objects.all()    
    #!! 사용자의 JLPT레벨 추가예정
    level = 5
    # 우선순위
    cnt = 0

    # 00시 날짜가 바뀌면 실행
    today_words = random_today_word(level)

     
    for one in today_words[0]:
        cnt += 1
        blank_word_positions = random_blank_positions(len(one.word), num_blanks=2)
        if blank_word_positions == 0:   
            blank_word = one.word[0]
        else:
            blank_word = ""
            for i in blank_word_positions:
                blank_word += one.word[i]

        if one.word:
            today_word = TodayWord.objects.create(
            dictionary= one,
            today_word = one.word,
            today_pronunciation = one.pronunciation,
            today_meaning=one.meaning,
            priority = cnt,
            #!! is_active > 오늘의 단어 설정완료 시 이전 단어 is_active = 0
            is_active = 1,
            # blank_word
            blank_word =   blank_word,            
            # POS
            today_Lv = one.Lv
        )
            

    test_word = 'カレンダー'
    blank_word = 'ンダ'
    today_words = []
    test_obj = Dictionary.objects.filter(word__contains = test_word)
    # filter 날짜 >  today_words > 우선순위 >
    today = timezone.now().date()
    today_words = TodayWord.objects.filter(date = today).order_by('priority')
    
    # rendered_word / blank_word
    # カレ__ー  / ンダ
    # 答_る / え
    # エ__ーター / レベ
    # 12시 > 오늘의 단어 db 저장
    

    context = {
        'blank_word': blank_word,
          # test단어 저장
        'today_words': today_words
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



