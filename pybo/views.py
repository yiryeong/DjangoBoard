from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer
from django.utils import timezone


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


@login_required(login_url='common:login')
def answer_create(request, question_id):
	"""
	pybo 답변 등록
	:param request:
	:param question_id: question 레코드 아이디
	:return:
	"""
	question = get_object_or_404(Question, pk=question_id)
	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			answer = form.save(commit=False)
			# request.user 현재 로그인한 계정의 User 모델 객체
			answer.author = request.user
			answer.create_date = timezone.now()
			answer.question = question
			answer.save()
			return redirect('pybo:detail', question_id=question.id)
	else:
		form = AnswerForm()
	context = {'question': question, 'form': form}
	return render(request, 'pybo/question_detail.html', context)


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


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
	"""
	답변 수정
	:param request:
	:param answer_id: 답변 레코드 아이디
	:return:
	"""
	answer = get_object_or_404(Answer, pk=answer_id)
	if request.user != answer.author:
		messages.error(request, '수정권한이 없습니다.')
		return redirect('pybo:detail', question_id=answer.question.id)

	if request.method == 'POST':
		form = AnswerForm(request.POST, instance=answer)
		if form.is_valid():
			answer = form.save(commit=False)
			answer.author = request.user
			answer.modify_date = timezone.now()
			answer.save()
			return redirect('pybo:detail', question_id=answer.question.id)
	else:
		form = AnswerForm(instance=answer)
	context = {'answer': answer, 'form': form}
	return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
	"""
	답변 삭제
	:param request:
	:param answer_id: 답변 레코드 아이디
	:return:
	"""
	answer = get_object_or_404(Answer, pk=answer_id)
	if request.user != answer.author:
		messages.error(request, '삭제권한이 없습니다.')
	else:
		answer.delete()
	return redirect('pybo:detail', question_id=answer.question.id)
