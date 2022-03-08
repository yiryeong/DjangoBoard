from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    # Question 모델에서 사용하는 author과 voter 필드가 모두 User 모델을 참조하고 있는데,
    # 추후 User.question_set과 같이 User 모델을 통해 Question데이터에 접근할 경우
    # author 필드를 기준으로 할지 voter 필드를 기준으로 할지 related_name 옵션을 추가하여 설정
    # 특정 사용자가 작성한 질문을 얻기 위해 some_user.author_question.all() 사용
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    # 글 1개에 여러 명이 추천할 수 있으며, 1명이 여러 개의 글을 추천 할 수 있어서 다대다 관계로 설정
    # 특정 사용자가 추천한 질문을 얻기 위한 코드는 some_user.voter_question.all()
    # ManyToManyField 필드는 중복을 허락하지 않는다.
    voter = models.ManyToManyField(User, related_name='voter_question')
    create_date = models.DateTimeField()
    # modify_date에 Null 허용
    # blank=True는 form.is_valid()를 통한 입력 폰 데이터 검사 시 값이 없어도 된다는 의미
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_answer')
    modify_date = models.DateTimeField(null=True, blank=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
