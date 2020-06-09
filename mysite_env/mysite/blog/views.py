from django.shortcuts import render,get_object_or_404
from .models import Blog,BlogType
from django.core.paginator import Paginator
from django.db.models import Count
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm

def get_blog_list_commen_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_NUMS_BLOGS)#每10篇进行分页
    page_num = request.GET.get('page',1) #获取url的页面参数（GET请求）判断是否有page属性 如果有默认值为1
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    page_range = list(range(max(1,current_page_num-2),min(paginator.num_pages,current_page_num+2)+1))
    if page_range[0] !=1:
        page_range.insert(0,1)
        if page_range[1] >=3:
            page_range.insert(1,"...")
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)
        if page_range[-2]<paginator.num_pages-2:
            page_range.insert(-1,"...")
    #获取分类blog
    
    '''blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)'''
    blog_date_list=Blog.objects.dates('created_time','month',order='DESC')
    blog_dates_list={}
    for blog_date in blog_date_list:
        blog_count=Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_list[blog_date]=blog_count



    context = {}
    context['page_range'] = page_range
    context['page_of_blogs'] =  page_of_blogs
    context['blog_types']=BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_list
    return context


def blog_list(request):
    blogs_all_list =Blog.objects.all()
    context=get_blog_list_commen_data(request,blogs_all_list)
    return render(request,'blog_list.html',context)


def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_filter_list=Blog.objects.filter(blog_type=blog_type)
    context=get_blog_list_commen_data(request,blog_filter_list)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    
    return render(request,'blogs_with_type.html',context)


def blogs_with_date(request,year,month):
    blogs_all_list =Blog.objects.filter(created_time__year=year, created_time__month=month)
    context=get_blog_list_commen_data(request,blogs_all_list)
    context['blog_with_date'] = '%s年%s月' %(year,month)
    return render(request,'blogs_with_date.html',context)


def blog_detail(request,blog_pk):
    blog=get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key=read_statistics_once_read(request,blog)
    blog_content_type=ContentType.objects.get_for_model(blog)
    comments=Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk)



    context = {}
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['comments'] = comments
    context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_pk})
    response = render(request,'blog_detail.html',context)
    response.set_cookie(read_cookie_key, 'true')#cookie记录 键和值 同时记录有效时间 max_age=60即一分钟内有效 expires=datetime在之前有效  
    return response
