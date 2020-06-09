from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm
'''def update_comment(request):
    referer=request.META.get('HTTP_REFERER',reverse('home'))
    user=request.user
    if not user.is_authenticated:
        return render(request,'error.html',{'message':'用户未登录！','redirect_to':referer})
    text=request.POST.get('text','').strip()
    if text == '':
        return render(request,'error.html',{'message':'评论内容为空！','redirect_to':referer})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class=ContentType.objects.get(model=content_type).model_class()#这里获取了Blog这个模型
        model_obj = model_class.objects.get(pk=object_id)#最终获取了被评论对象
    except Exception as e:
        return render(request,'error.html',{'message':'评论对象不存在','redirect_to':referer})

    comment=Comment()
    comment.text=text
    comment.user=user
    comment.content_object=model_obj
    
    comment.save()
    
    return redirect(referer)'''
def update_comment(request):
    referer=request.META.get('HTTP_REFERER',reverse('home'))
    comment_form = CommentForm(request.POST,user=request.user)
    if comment_form.is_valid():
        comment=Comment()
        comment.user=comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object=comment_form.cleaned_data['content_object']
        comment.save()
        return redirect(referer)
    else:
        return render(request,'error.html',{'message':comment_form.errors,'redirect_to':referer})