from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from ..models import Question
from ..forms import QuestionForm


@login_required(login_url='common:login')
def question_create(request):
    """
        pybo 질문 등록
        :param request:
        :return:
    """

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # 요청 받은 form이 유효한지 검사
        if form.is_valid():
            # commit=False는 임시 저장을 의미하며 데이터가 실제 저장 되지 않는다.
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        # method == 'GET'
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
        pybo 질문 수정
        :param request:
        :param question_id: 질문 레코드 아이디
        :return:
    """

    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == 'POST':
        # question을 기본값으로 하여 화면으로 전달받은 입력값들을 덮어써서 QuestionForm을 생성하라는 의미
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        # instance=question 지정하면 기존 값을 폼에 채울 수 있다.
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
        pybo 질문 삭제
        :param request:
        :param question_id: 질문 레코드 아이디
        :return:
    """

    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')
