from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,redirect
from compile.models import age,position,sex,actor_number,product_option,content,script_type,play
from artist.models import task,video
from django.core import serializers 
from django.http import HttpResponse
import datetime
import json
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.conf import settings  
from lanlanTest21.settings import STATICFILES_DIRS
import os 
from app01.models import journal1

def journal(request):
    compilename=request.session.get("username")
    action=request.session.get("action")
    time=request.session.get("now_time")
    jour=journal1(journal_name=compilename,journal_action=action,journal_time=time)
    jour.save()

def artist_show(request):
    username=""
    if request.GET:
        username=request.GET["username"]  
    else:
        username=request.session.get("username")
        
    if request.session.get("status1"):
        request.session["username"]=username  
        tasks=task.objects.filter(Q(uname=username) & ~Q(task_status="审核通过"))
        page = request.POST.get('page')
        paginator = Paginator(tasks, 3)
        try:
            rows = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            rows = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            rows = paginator.page(paginator.num_pages)
        now_time=datetime.datetime.today()
        request.session["action"]="演员登陆"
        request.session["now_time"]=str(now_time)
        journal(request)
        return render(request,"artist/artist_index.html",{"username":username,"tasks":rows})
    else:
        return redirect("/index")
def search_article(request):
    ages=age.objects.all()
    positions=position.objects.all()
    sexs=sex.objects.all()
    actor_numbers=actor_number.objects.all()
    product_options=product_option.objects.all()
    contents=content.objects.all()
    script_types=script_type.objects.all()
    author="456"
    age_id = request.POST.get("age")
    Position_id =  request.POST.get("Position")
    sex_id =  request.POST.get("sex")
    actor_numbers_id = request.POST.get("actor_numbers")
    product_options_id = request.POST.get("product_options")
    content_type_id = request.POST.get("content_type")
    script_types_id = request.POST.get("script_types")
    
    now_time=datetime.datetime.today()
    request.session["action"]="搜索条件:"+" "+age_id+" "+Position_id+" "+sex_id+" "+actor_numbers_id+" "+product_options_id+" "+content_type_id+" "+script_types_id
    request.session["now_time"]=str(now_time)
    journal(request)
    
    plays=play.objects.filter(Q(play_age_id=age_id) & Q(play_position_id=Position_id) &
                        Q(play_sex_id=sex_id) & Q(play_actor_number_id=actor_numbers_id) &
                        Q(play_product_option_id=product_options_id) & Q(play_content_id=content_type_id) &
                        Q(play_script_type_id=script_types_id) & Q(author=author))
    paginator = Paginator(plays,1) 
    try: 
        num = request.GET.get('index','1') 
        number = paginator.page(num)
    except PageNotAnInteger: 
        number = paginator.page(1) 
    except EmptyPage: 
        number = paginator.page(paginator.num_pages) 
    dict1={
        "ages":ages,
        "positions":positions,
        "sexs":sexs,
        "actor_numbers":actor_numbers,
        "product_options":product_options,
        "contents":contents,
        "script_types":script_types,
        'page':number,
        "articles":paginator
        }
    return render(request,"artist/get_play.html",dict1)

def get_play(request):
    if request.session.get("status1"):
        ages=age.objects.all()
        positions=position.objects.all()
        sexs=sex.objects.all()
        actor_numbers=actor_number.objects.all()
        product_options=product_option.objects.all()
        contents=content.objects.all()
        script_types=script_type.objects.all()
        plays=play.objects.all()
        paginator = Paginator(plays,2,1) 
        num = request.POST.get('page',"1")
        try: 
            number = paginator.page(num)
        except PageNotAnInteger: 
            number = paginator.page(1) 
        except EmptyPage: 
            number = paginator.page(paginator.num_pages) 
        dict1={
            "ages":ages,
            "positions":positions,
            "sexs":sexs,
            "actor_numbers":actor_numbers,
            "product_options":product_options,
            "contents":contents,
            "script_types":script_types,
            'rows':number,
            "articles":paginator
            }
        now_time=datetime.datetime.today()
        request.session["action"]="查看所有剧本"
        request.session["now_time"]=str(now_time)
        journal(request)
        return render(request,"artist/get_play.html",dict1)
    else:
        return redirect("/index")
    
# 提交任务    有     剧本id   视频id    产品id   当前状态（未提交视频，提交视频未审核，审核通过，审核失败（失败原因））    提交时间    


today=datetime.datetime.today()
def Allods_Gold(request):
    username=request.POST.get("username")
    sc_id=request.POST.get("sc_id")
    status="任务领取成功"    
    if task.objects.filter(Q(uname=username) & Q(aid=sc_id)):
        status="任务已经领取过了，请选择别的剧本或产品"
        return HttpResponse(json.dumps({
                    "status": status
                }))
    else:
        pid=1
        p=task(uname=username,aid_id=sc_id,pid_id=pid,upload_time=today)
        p.save()
        
        plays=play.objects.filter(id=sc_id)
        for p in plays:
            play.objects.filter(id=sc_id).update(Script_usage=p.Script_usage+1)
        
        return HttpResponse(json.dumps({
                    "status": status
                }))
        
    
    
    
from django.http import HttpResponse

# 视频上传。
def upload_video(request):
    try:
        f1 = request.FILES.get('video')
        uploadid=request.POST.get("uploadid")
        uname=request.POST.get("uploadname")
        productname=request.POST.get("uploadproduct")
        p = video()
        p.video_title=f1.name
        p.video_path="/video/%s/"%uname + f1.name
        p.video_product=productname
        p.video_author=uname
        p.save()
        try:
            fname = str(STATICFILES_DIRS[0]) + "/video/%s/"%uname + f1.name
            with open(fname,'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
        except:
            os.makedirs(str(STATICFILES_DIRS[0]) + "/video/%s/"%uname) 
            fname = str(STATICFILES_DIRS[0]) + "/video/%s/"%uname + f1.name
            with open(fname,'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
        now_time=datetime.datetime.today()
        request.session["action"]="任务id："+uploadid+"  成功上传视频："+f1.name+" 保存地址 "+str(STATICFILES_DIRS[0]) + "/video/%s/"%uname + f1.name
        request.session["now_time"]=str(now_time)
        journal(request)
        videos=video.objects.filter(video_title=f1.name)
        for i in videos:
            task.objects.filter(id=uploadid).update(vid=i.id)
        task.objects.filter(id=uploadid).update(task_status="成功提交视频，等待审核")
        username=request.session.get("username")
        return HttpResponseRedirect("/artist_show?username=%s"%username)
    except:
        username=request.session.get("username")
        return  HttpResponse("请选择文件<a href='/artist_show?username=%s''>返回页面</a>"%username)
    
#     ajax上传   错误在于文件上传很慢，，以及读取方面
def upvideo(request):
    f1 = request.FILES.get('video')
    uploadid=request.POST.get("uploadid")
    uname=request.POST.get("uploadname")
    productname=request.POST.get("uploadproduct")
    p = video()
    p.video_title=f1.name
    p.video_path="/%s/video/"%uname + f1.name
    p.video_product=productname
    p.video_author=uname
    p.save()
    try:
        fname = settings.MEDIA_ROOT + "/%s/video/"%uname + f1.name
        with open(fname,'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
    except:
        os.makedirs(settings.MEDIA_ROOT + "/%s/video/"%uname) 
        fname = settings.MEDIA_ROOT + "/%s/video/"%uname + f1.name
        with open(fname,'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
    task.objects.filter(id=uploadid).update(task_status="成功提交视频，等待审核")
    status="上传成功"
    return HttpResponse(json.dumps({
                "status": status
            }))
    
    
def del_task(request):
    sc_id=request.POST.get("sc_id1")  
    tasks = task.objects.filter(id=sc_id)  # 执行删除操作
    tasks.delete()
    status="删除成功"
    
    now_time=datetime.datetime.today()
    request.session["action"]=status
    request.session["now_time"]=str(now_time)
    journal(request)
    
    return HttpResponse(json.dumps({"status": status}))





# 查看任务审核通过之后，艺人可以看到的任务
def get_audit(request):
    username=request.POST.get("username")
    task_list=task.objects.filter(Q(uname=username) & Q(task_status="审核通过")).order_by("-upload_time")[:10]
    test_obj_list = serializers.serialize('json', task_list )
    alarm_match_json_list = [test_obj["fields"] for test_obj in json.loads(test_obj_list )]
    return HttpResponse(json.dumps({ "status": alarm_match_json_list}))
    
    
    
    
def sadhskajsh(request):
    sc_id=request.POST.get("id")
    return HttpResponse("1456")
    
    
def get_title(request):
    sc_id1=request.POST.get("sc_id1")
    palys=play.objects.filter(id=sc_id1)
    for p in palys: 
        return HttpResponse(json.dumps({"palys":p.script_title}))
    


from artist.models import product
def get_product(request):
    sc_id2=request.POST.get("sc_id2")
    products=product.objects.filter(id=sc_id2)
    for p in products: 
        return HttpResponse(json.dumps({"pname":p.name}))    
    
    
    
    
def look_all(request):
    username=""
    if request.GET:
        username=request.GET["username"]  
    else:
        username=request.session.get("username")
    request.session["username"]=username
    tasks=task.objects.filter(Q(uname=username) & Q(task_status="审核通过"))
    
    now_time=datetime.datetime.today()
    request.session["action"]="查看所有任务"
    request.session["now_time"]=str(now_time)
    journal(request)
    
    page = request.POST.get('page')
    paginator = Paginator(tasks, 3)
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        rows = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        rows = paginator.page(paginator.num_pages)
    return render(request,"artist/all_task.html",{"tasks":rows})
    
    
    
    
    
    
    
    
    
    
    
    
   