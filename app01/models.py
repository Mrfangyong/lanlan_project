from django.db import models
from lxml.html.builder import SUP

# Create your models here.

class user(models.Model):
    role=(
        ('scriptwriter','编剧'),
        ('Administrator','管理员'),
        ('actor','艺人'),
        ('audit','审核')
        )
    state=(
        ('terminate_agreement ','解约'),
        ('normal','正常')
        )
    name=models.CharField(max_length=255)
    tel=models.CharField(max_length=255)
    password=models.CharField(max_length=225)
    role_type=models.CharField(max_length=225,choices=role,default="艺人")
    register_time=models.DateField(auto_now_add=True)
    user_state=models.CharField(max_length=225,choices=state,default="正常")
    
class mistake(models.Model):
    mistake_content=models.CharField(max_length=225)
    mistake_time=models.DateTimeField(auto_now_add=True)
    


class journal1(models.Model):
    journal_name=models.CharField(max_length=225)
    journal_action=models.CharField(max_length=225)
    journal_time=models.DateTimeField(auto_now_add=True)
    
    
    
# 重中之重    
class AnailManger(models.Manager):
    def get_queryset(self):
        return super(AnailManger,self).get_queryset().filter(is_delete=False)
    def get_count(self):
        return super(AnailManger,self).get_queryset().count()
    def create_mdoel(self,name="moren"):
        a=self.model()
        a.name=name
        return a
    
class Student(models.Model): 
    name=models.CharField(max_length=200)
    is_delete=models.BooleanField(default=False)
#     a_m=AnailManger()   
    







