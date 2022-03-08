from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count

from ..models import Question


def index(request):
    """
        질문 목록 출력
        :param request:
        :return:
    """

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    if so == 'recommend':
        # annotate 함수는 Question 모델의 기존 필드인 author, subject, content, create_date, modify_date, voter에 질문의 추천 수에 해당하는 num_voter필드를 임시로 추가해 주는 함수
        # 이렇게 annotate함수로 nom_voter필드를 추가하면 filter 함수나 order_by 함수에서 num_voter 필드를 사용할 수 있게 된다.
        # Count('voter')는 해당 질문의 추천 수이다.
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    if kw:
        # Q 함수에 사용된 subject__icontains=kw 는 제목에 kw 문자열이 포함되었는지를 의미
        question_list = question_list.filter(
            Q(subject__icontains=kw) |   # 제목 검색
            Q(content__icontains=kw) |   # 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)   # 답변 글쓴이 검색
        ).distinct()

    # paging
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여 주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
        특정 질문 내용 출력
        :param request:
        :param question_id: 질문 레코드 아이디
        :return:
    """
    page = request.GET.get('page', '1')
    question = get_object_or_404(Question, pk=question_id)

    # paging
    answers = question.answer_set.all()
    paginator = Paginator(answers, 2)  # 페이지당 2개씩 보여 주기
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answers': page_obj, 'page': page}

    return render(request, 'pybo/question_detail.html', context)
