import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


@register.filter()
def mark(value):
    # 해당 함수는 markdown 모듈과 mark_safe 함수를 이용항 문자열을 HTML 코드로 변환하여 반환한다. 
    # 'nl2br'은 줄바꿈 문자를( Enter 포함 ) ,<br> 태그로 바꿔준다.
    #  'nl2br' 이부분을 설정하지 않을 경우 줄바꿈을 위해 줄 끝에 마크다운 문법인 스페이스를 2개 연속으로 입력해야 한다.
    extensions = ['nl2br', 'fenced_code']
    return mark_safe(markdown.markdown(value, extensions=extensions))
