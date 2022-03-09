from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.hashers import check_password #평문을 암호화했을 때 비문이라면 True, 아니면 False가 나온다. 
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'acc/index.html')

def login_user(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        user = authenticate(username=un, password=up)
        if user :
            login(request,user)
            messages.success(request, f"{user} 님 환영합니다.")
            return redirect('acc:index')
        else:
            messages.error(request,'계정정보가 일치하지 않습니다.')
    return render(request,'acc/login.html')

def logout_user(request):
    logout(request)
    return redirect('acc:index')

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        ua = request.POST.get("uage")
        uc = request.POST.get("ucom")
        upic = request.FILES.get("upic")
        try:
            User.objects.create_user(username=un, password=up, age=ua, comment = uc, pic = upic)
            return redirect('acc:login')
        except:
            messages.info(request, '이미 존재하는 아이디 입니다.')

    return render(request,'acc/signup.html')


def profile(request):
    return render(request,'acc/profile.html')

def delete(request):
    u = request.user
    ck = request.POST.get("pwck")
    if check_password(ck, u.password ):
        u.pic.delete()
        u.delete() # user 가 삭제 돼도 사진이 삭제 되지는 않는다. 사진 별도로 삭제  
        return redirect('acc:index')
    else:
        messages.error(request,'패스워드가 일치하지 않습니다.')
    return redirect('acc:profile')



def update(request):
    if request.method == "POST":
        u = request.user
        up = request.POST.get("upass")
        ua = request.POST.get("uage")
        uc = request.POST.get("ucom")
        pi = request.FILES.get("upic")
        if up :
            u.set_password(up)
        u.age = ua
        u.comment = uc
        if pi : 
            u.pic.delete()
            # 기존 이미지 삭제 후 변경된 이미지 저장 
            u.pic = pi
        u.save()
        login(request, u)
        return redirect('acc:profile')
    return render(request,'acc/update.html')
