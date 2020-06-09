import datetime
from django.shortcuts import render,redirect
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from read_statistics.utils import get_seven_days_read_date,get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog
from .forms import LoginForm,RegForm

def get_7days_hot_data():
    today=timezone.now().date()
    date=today-datetime.timedelta(days=7)
    blogs=Blog.objects.filter(read_detail__date__lt=today, read_detail__date__gte=date)\
            .values('id','title')\
            .annotate(read_num_sum=Sum('read_detail__read_num'))\
            .order_by('-read_num_sum')
    return blogs[:3]




def home(request):
    blog_content_type=ContentType.objects.get_for_model(Blog)
    read_seven_num,dates=get_seven_days_read_date(blog_content_type)
    hot_data_for_7days=cache.get('hot_data_for_7days')
    if hot_data_for_7days is None:
        hot_data_for_7days = get_7days_hot_data()
        cache.set('hot_data_for_7days',hot_data_for_7days,3600)
    hot_data_for_yesterday=cache.get('hot_data_for_yesterday')
    if hot_data_for_yesterday is None:
        hot_data_for_yesterday=get_yesterday_hot_data(blog_content_type)
        cache.set('hot_data_for_yesterday', hot_data_for_yesterday, 3600)
    context={}
    context['read_seven_num']=read_seven_num
    context['dates']=dates
    context['read_today_hot'] = get_today_hot_data(blog_content_type)
    context['read_yesterday_hot'] = hot_data_for_yesterday
    context['hot_data_for_7days'] =  hot_data_for_7days 
    return render(request,'home.html',context)


def login(request):
    if request.method == 'POST':#这里是点击登录之后的读取验证信息
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:        
        login_form = LoginForm()#此处是呈现空的输入框

    context={}
    context['login_form']=login_form
    return render(request,'login.html',context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username=reg_form.cleaned_data['username']
            email=reg_form.cleaned_data['email']
            password=reg_form.cleaned_data['password']
            
            user=User.objects.create_user(username,email,password)
            user.save()

            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))

    else:
        reg_form=RegForm()

    context={}
    context['reg_form']=reg_form
    return render(request,'register.html',context)
