from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.

def login(request):
    if request.method == 'POST': #POST 요청이 들어오면 login 시켜주고
        username = request.POST['username']
        password = request.POST['password']

        #User Model에 username, password가 일치하는 객체 있으면 데려오고 없으면 None을 반환해
        user = auth.authenticate(request, username=username, password=password)

        #none이 아니라면, 로그인시켜
        if user is not None:
            auth.login(request,user)
            return redirect('main:mainpage')
        
        #none이라면 다시 login 화면으로 돌아가
        else:
            return render(request,'accounts/login.html')

        pass
    elif request.method == 'GET': #GET 요청이 들어오면 login.html 보여줘
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request) #현재 로그인 유저 로그아웃 처리
    return redirect('main:mainpage')

def signup(request):
    if request.method == 'POST':

        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password']

            )
            nickname=request.POST['nickname']
            department=request.POST['department']
            birthday=request.POST['birthday']
            mbti=request.POST['mbti']

            profile = Profile(user=user, nickname=nickname, department=department, birthday=birthday, mbti=mbti)
            profile.save()

            auth.login(request,user)
            return redirect('/')
        
    return render(request, 'accounts/signup.html')