from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from ..models import Question


def index(request):
    """
        질문 목록 출력
        :param request:
        :return:
    """

    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    # paging
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
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
