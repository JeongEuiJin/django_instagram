from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import HttpResponse
from django.shortcuts import render, redirect


def login(request):
    # member/login.html생성
    # username , password,button이 있는 html생성
    # post요청이 올 경우 좌측 코드를 기반으로 로그인 완료 후 post_list이동
    # 실패할 경우 httpresponse로 login invalid!띄워주기

    # member/urls.py 생성
    #   /member/login/으로 접근시 이 view로 오도록 설정
    #   config/urls.py에 member/urls.py를 include
    #       member/urls.py에 app_name설정으로 namespace지정
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            django_login(request, user)
            return redirect('post:post_list')
        else:
            return HttpResponse('Logins credentaials invalid')


    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')
        return render(request, 'member/login.html')


def logout(request):
    django_logout(request)
    return redirect('post:post_list')
