from django.shortcuts import render, get_object_or_404, redirect
from .forms import QuestionForm, AnswerForm
from .models import Question
from django.utils import timezone


def index(request):
	"""
	질문 목록 출력
	:param request:
	:return:
	"""
	question_list = Question.objects.order_by('-create_date')
	context = {'question_list': question_list}
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
			answer.create_date = timezone.now()
			answer.question = question
			answer.save()
			return redirect('pybo:detail', question_id=question.id)
	else:
		form = AnswerForm()
	context = {'question': question, 'form': form}
	return render(request, 'pybo/question_detail.html', context)


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
			question.create_date = timezone.now()
			question.save()
			return redirect('pybo:index')
	else:
		# method == 'GET'
		form = QuestionForm()
	context = {'form': form}
	return render(request, 'pybo/question_form.html', context)
