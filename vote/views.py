from django.shortcuts import render, redirect
from .models import Topic,Choice
from django.utils import timezone
# Create your views here.

def index(request):
    t = Topic.objects.all()
    t = t.order_by('-pubdate')
    context  = {
        'tset' : t
     }
    return render(request,'vote/index.html', context)

def detail(request,tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    context = {
        'T' : t,
        'cset': c,
    }
    return render(request,'vote/detail.html',context)

def vote(request,tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        t.voter.add(request.user)
        cpk = request.POST.get('ch')
        c = Choice.objects.get(id=cpk)
        c.choicer.add(request.user)
    return redirect('vote:detail',tpk)

def cancel(request,tpk):
    t = Topic.objects.get(id=tpk)
    t.voter.remove(request.user) #투표 안한 사람으로 만듬
    # 나를 참조하고 있는 보기들 중에 user가 있으면 빼내는 방법(가장 직관적)
    # cset = t.choice_set.all()
    # for i in cset:
    #     if request.user in i.choicer.all():
    #        i.choicer.remove(request.user)
    #        break
    # user입장에서 내가 고른 보기들 중에 topic이 t인 친구를 고르는 것
    request.user.choice_set.get(topic=t).choicer.remove(request.user)
    # => choice중에 topic이 t인 choice의 레코드  
    return redirect('vote:detail',tpk)


def create(request):
    if request.method == "POST" : 
        s = request.POST.get('sub')
        c = request.POST.get('con')
        cn = request.POST.getlist('cname')
        cp = request.FILES.getlist('cpic')
        cc = request.POST.getlist('ccom')
        if len(cn) > 1:
            t = Topic(subject=s, content=c, maker=request.user, pubdate=timezone.now())
            t.save()
            for name, pic, com in zip(cn, cp, cc):
                #zip = 각 list 압축
                Choice(topic=t, chname=name, chpic=pic, chcom=com).save()
            return redirect('vote:index')
    return render(request,'vote/create.html')

