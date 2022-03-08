from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from ..models import Question


def index(request):
    """
        질문 목록 출력
        :param request:
        :return:
    """

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

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

    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
        특정 질문 내용 출력
        :param request:
        :param question_id: 질문 레코드 아이디
        :return:
    """

    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
