from django.db import models
from compile.models import product_option,play
from app01.models import user
# Create your models here.
# id    任务id
# uid    用户id
# aid    剧本id
# vid    视频id
# pid    产品id
# task_status     任务状态
# upload_time    提交时间
class product(models.Model):
    name=models.CharField(max_length=255)
    product_price=models.CharField(max_length=255)
    product_path=models.CharField(max_length=255)

class video(models.Model):
    video_title=models.CharField(max_length=255)
    video_path=models.CharField(max_length=255)
    video_product=models.CharField(max_length=255)
    video_author=models.CharField(max_length=255)

 
# 提交任务    有     剧本id   视频id    产品id   当前状态（未提交视频，提交视频未审核，审核通过，审核失败（失败原因））    提交时间

class task(models.Model):
    uname=models.CharField(max_length=255)
    aid=models.ForeignKey(play,on_delete=models.CASCADE)
    vid=models.IntegerField(default="0")
    pid=models.ForeignKey(product,on_delete=models.CASCADE)
    task_status=models.CharField(max_length=255,default="未提交视频")
    upload_time=models.DateTimeField(auto_now_add=True)
    
    
class approved_memo(models.Model):
    tid=models.ForeignKey(task,on_delete=models.CASCADE)
    audit_user=models.CharField(max_length=255)
    audit_time=models.DateTimeField(auto_now_add=True)
     
# id    任务id
# uname    成员名字
# aid    剧本id
# vid    视频id
# pid    产品id
# task_status     任务状态
# upload_time    提交时间



# class task(models.Model):



















    