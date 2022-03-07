from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm


def signup(request):
    """
    회원가입
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # .is_valid() 를 통해서 검증에 통과한 값은 cleaned_data 변수명으로 사전타입 으로 제공된다.
            username = form.cleaned_data.get('username')   # form.cleaned_data['username']
            raw_password = form.cleaned_data.get('password1')
            # authenticate, login 함수는 django.contrib.auth  패키지에 있는 함수로 사용자 인증과 로그인을 담당한다.
            # 회원가입이 완료 된 이후에 자동으로 로그인 되도록 authenticate, login 함수 사용
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
