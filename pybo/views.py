from django.shortcuts import render, get_object_or_404
from .models import Question


def index(request):
	"""
	pybo 목록 출력
	:param request:
	:return:
	"""
	question_list = Question.objects.order_by('-create_date')
	context = {'question_list': question_list}
	return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
	"""
	pybo 내용 출력
	:param request:
	:param question_id: 질문 레코드 아이디
	:return:
	"""
	question = get_object_or_404(Question, pk=question_id)
	context = {'question': question}
	return render(request, 'pybo/question_detail.html', context)
