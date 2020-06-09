import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from .models import ReadNum,ReadDetail


def read_statistics_once_read(request,obj):
    ct=ContentType.objects.get_for_model(obj)
    key="%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        #总阅读数
        readnum,create=ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readnum.read_num+=1
        readnum.save()
    #当天阅读数
        date=timezone.now().date()
        readDetail,create =  ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        readDetail.read_num+=1
        readDetail.save()


    return key


def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    read_sums=[]
    dates=[]
    for i in range(7, 0, -1):
        date=today-datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details=ReadDetail.objects.filter(content_type=content_type,date=date)
        #这里会查询到多种数据，需要聚合计算
        rs=read_details.aggregate(read_num_sum=Sum('read_num'))#返回的值是一个字典
        read_sums.append(rs['read_num_sum'] or 0)
    return read_sums,dates


def get_today_hot_data(content_type):
    today=timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:3]

def get_yesterday_hot_data(content_type):
    today=timezone.now().date()
    yesterday=today-datetime.timedelta(days=1)
    read_details= ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:3]


