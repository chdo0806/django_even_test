from django.shortcuts import render,redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.

def index(request):
    pg = request.GET.get("page",1)
    kw = request.GET.get("kw")
    cate = request.GET.get("cate")
    if kw :
        if cate == "sub" :
            b = Board.objects.filter(subject_contains=kw)
        elif cate == "wri" :
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer_contains=u)
            except:
                b = Board.objects.none()
        elif cate == "con" :
            b = Board.objects.filter(content_contains=kw)  
        else:  
            messages.error(request,'혼나!')
            b = Board.objects.all()
    else:
        b = Board.objects.all()

    b = b.order_by('-pubdate') # 최신 글 부터 정렬 
    pag = Paginator(b,5)
    obj = pag.get_page(pg)
    context = {
        "bset" : obj,
        "cate" : cate,
        "kw" : kw,
    }
    return render(request,'board/index.html', context)

def detail(request,bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
        # 나한테 댓글 단 사람 다 나와.
    context = {
        "b" : b,
        "rset" : r
    }

    return render(request,'board/detail.html',context)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect('board:detail',bpk)

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect('board:detail',bpk)


def creply(request,bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(b=b, replyer=request.user, comment=c, pubdate=timezone.now()).save()
    return redirect('board:detail',bpk)


def dreply(request,bpk,rpk):
    r = Reply.objects.get(id=rpk)
    if request.user == r.replyer :
        r.delete()
    else:
        messages.warning(request,"삭제할 수 없는 댓글입니다.")
    return redirect('board:detail',bpk)



def delete(request,bpk):
    b = Board.objects.get(id=bpk)
    if  request.user == b.writer :
        b.delete()
    else:
        messages.error(request,'혼나!')
    return redirect('board:index')

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        if s and c :
            Board(subject=s, content=c, writer=request.user, pubdate=timezone.now()).save()
            # from djang.utils import timezone -> 시간 적용
            return redirect('board:index')
    return render(request,'board/create.html')



def update(request,bpk):
    b = Board.objects.get(id=bpk)
    # 자신의 글이 아니면 board의 index로 이동
    if b.writer != request.user :
        messages.error(request, f"{request.user}님이 작성한 글이 아닙니다.")
        return redirect('board:index')

    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")

        if s and c:
            b.subject = s
            b.content = c
            b.save()
            return redirect('board:detail', bpk)

    context = {
        'b' : b
    }
    return render(request,'board/update.html',context)


    
