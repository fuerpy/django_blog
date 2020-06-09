from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import ReadNumExpandMethod,ReadDetail



class BlogType(models.Model):
    type_name=models.CharField(max_length=30)

    def __str__(self):
        return self.type_name




class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=36)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time=models.DateTimeField(auto_now_add=True)
    last_updated_time=models.DateTimeField(auto_now=True)
    read_detail=GenericRelation(ReadDetail)
    

    

    def __str__(self):
        return 'Blog: %s' % self.title

    class Meta:
        ordering = ['-created_time']


'''class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog=models.OneToOneField(Blog,on_delete=models.DO_NOTHING)'''
    

# Create your models here.
