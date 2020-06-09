from django.urls import path
from . import views

urlpatterns = [
    #http://localhost:8000/blog/1
    path('update_comment',views.update_comment,name='update_comment'),
]
