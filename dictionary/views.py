from django.shortcuts import render
from .models import Dictionary, TodayWord


# Create your views here.
def dictionary(request):
    dictionary = Dictionary.objects.all()

    # 00시에 오늘의 단어 / 가로세로퀴즈 자동업데이트 
    test_word = '答える'
    test_obj = Dictionary.objects.filter(word__contains = test_word)
    
    if test_word:
        today_word = TodayWord.objects.create(
            dictionary=test_obj[0],
            today_word = test_obj[0].word,
            today_pronunciation = test_obj[0].pronunciation,
            today_meaning=test_obj[0].meaning

        )

    return render(request, 'dictionary/dictionary.html')

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



