from django.shortcuts import render,redirect
from compile.models import play,age,position,sex,actor_number,product_option,content,script_type
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import datetime
from django.http import HttpResponse
import json
from django.db.models import Q
from django.core import serializers 
from django.db import connection
from app01.models import journal1

def journal(request):
    compilename=request.session.get("compilename")
    action=request.session.get("action")
    time=request.session.get("now_time")
    jour=journal1(journal_name=compilename,journal_action=action,journal_time=time)
    jour.save()
    
# 谁  干了什么  时间


def compile_show(request):
    try:
        compilename=""
        if request.GET:
            compilename=request.GET["compilename"]  
        else:
            compilename=request.session.get("compilename")
        request.session["compilename"]=compilename

        play1=play.objects.filter(Q(author=compilename) & Q(Script_usage=0))
        page1 = request.POST.get('page')
        paginator = Paginator(play1,2)
        try:
            rows = paginator.page(page1)
        except PageNotAnInteger:
            rows = paginator.page(1)
        except EmptyPage:
            rows = paginator.page(paginator.num_pages)
        cont={
            'compilename':compilename,
            'page':rows,
            }
        now_time=datetime.datetime.today()
        request.session["action"]="编剧登陆"
        request.session["now_time"]=str(now_time)
        journal(request)
        return render(request,"compile/compile_index.html",cont)
    except Exception as e:
        return render(request,"login/404.html",{"mistake":e})   

def upload_article(request):
    try:
        age=request.POST.get("age")
        Position=request.POST.get("Position")
        sex=request.POST.get("sex")
        actor=request.POST.get("actor")
        product=request.POST.get("product")
        content=request.POST.get("content")
        script=request.POST.get("script")
        title=request.POST.get("title")
        compilename=request.session.get("compilename")
        cont=request.POST.get("cont")
        today=datetime.datetime.today()
        plays=play(script_title=title,script_content=cont,upload_time=today,author=compilename,play_age_id=int(age),play_position_id=Position,
                   play_sex_id=sex,play_actor_number_id=actor,play_product_option_id=product,play_content_id=content,play_script_type_id=script)
        status = "上传成功"
        result="上传失败,请查看内容格式"
        if plays.save():
                now_time=datetime.datetime.today()
                request.session["action"]=title+"上传成功"
                request.session["now_time"]=str(now_time)
                journal(request)
                return HttpResponse(json.dumps({"status": status}))
        else:
                now_time=datetime.datetime.today()
                request.session["action"]=title+"上传成功"
                request.session["now_time"]=str(now_time)
                journal(request)
                return HttpResponse(json.dumps({"result": result}))  
    except Exception as e:
        return render(request,"login/404.html",{"mistake":e})   
    
def check_content(request):
    try:
        sc_id=request.POST.get("sc_id1")
        plays=play.objects.filter(id=sc_id)
        for p in plays:
            return HttpResponse(json.dumps({
                "script_content":p.script_content,
                "upload_time":str(p.upload_time),
                "script_title":p.script_title,
                "author":p.author,
                "Script_usage":p.Script_usage,
                "play_age":p.play_age.age_section,
                "play_position":p.play_position.Position_type,
                "play_sex":p.play_sex.sex_option,
                "play_actor_number":p.play_actor_number.actor_numbers,
                "play_product_option":p.play_product_option.product_options,
                "play_content":p.play_content.content_type,
                "play_script_type":p.play_script_type.script_types,
                }))
    except Exception as e:
        return render(request,"login/404.html",{"mistake":e})   
    

def refresh_article(request):
    try:
        click_nums=request.POST.get("click_nums")
        start_limit_nums=int(click_nums)*50+1
        end_limit_nums=start_limit_nums+50
        sql="SELECT script_title FROM compile_play WHERE id BETWEEN %s AND %s"%(start_limit_nums,end_limit_nums)
        cursor=connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        name=[]
        for k in results:
            name.append("".join(k))
        return HttpResponse("6666")
    except Exception as e:
        return render(request,"login/404.html",{"mistake":e})   
        




def del_article(request):
    try:
        sc_id=request.POST.get("sc_id1")
        plays=play.objects.filter(id=sc_id)
        plays.delete()
        status="删除成功"
        now_time=datetime.datetime.today()
        request.session["action"]=sc_id+"  "+status
        request.session["now_time"]=str(now_time)
        journal(request)
        return HttpResponse(json.dumps({"status": status}))
    except Exception as e:
        return render(request,"login/404.html",{"mistake":e})   
def update_article(request):
    try:
        sc_id=request.GET.get("sc_id")
        plays=play.objects.filter(id=sc_id)
        ages=age.objects.all()
        positions=position.objects.all()
        sexs=sex.objects.all()
        actor_numbers=actor_number.objects.all()
        product_options=product_option.objects.all()
        contents=content.objects.all()
        script_types=script_type.objects.all()
        dict1={
            "plays":plays,
            "ages":ages,
            "positions":positions,
            "sexs":sexs,
            "actor_numbers":actor_numbers,
            "product_options":product_options,
            "contents":contents,
            "script_types":script_types,
            }
        return render(request,"compile/update_article.html",dict1)
    except Exception as e:
        return render(request,"login/404.html",{"mistake":e})   
def update_db_article(request):
    try:
        ids=request.POST.get("ids")
        age=request.POST.get("age")
        Position=request.POST.get("Position")
        sex=request.POST.get("sex")
        actor=request.POST.get("actor")
        product=request.POST.get("product")
        content=request.POST.get("content")
        script=request.POST.get("script")
        title=request.POST.get("title")
        cont=request.POST.get("cont")
        now_time=datetime.datetime.now().strftime('%Y-%m-%d')
        play.objects.filter(id=ids).update(script_title=title)
        play.objects.filter(id=ids).update(script_content=cont)
        play.objects.filter(id=ids).update(upload_time=now_time)
        play.objects.filter(id=ids).update(play_age=age)
        play.objects.filter(id=ids).update(play_position=Position)
        play.objects.filter(id=ids).update(play_sex=sex)
        play.objects.filter(id=ids).update(play_actor_number=actor)
        play.objects.filter(id=ids).update(play_product_option=product)
        play.objects.filter(id=ids).update(play_script_type=script)
        status="修改成功"
        now_time=datetime.datetime.today()
        request.session["action"]=status
        request.session["now_time"]=str(now_time)
        journal(request)
        return HttpResponse(json.dumps({"status": status}))
    except Exception as e:
        return render(request,"login/404.html",{"mistake":e})   

def get_compile(request):
    try:
        username=request.POST.get("username")
        plays=play.objects.filter(Q(author=username) & Q(Script_usage__gt=0))
        test_obj_list = serializers.serialize('json', plays )
        alarm_match_json_list = [test_obj["fields"] for test_obj in json.loads(test_obj_list )]
        return HttpResponse(json.dumps({"status": alarm_match_json_list}))
    except Exception as e:
        return render(request,"login/404.html",{"mistake":e})   
def actual(request):
    script_title1=request.POST.get("sc_id1")
    now_time=datetime.datetime.today()
    request.session["action"]=script_title1+"查看"
    request.session["now_time"]=str(now_time)
    journal(request)
    plays=play.objects.filter(script_title=script_title1)
    try:
        for p in plays:
            return HttpResponse(json.dumps({
                "script_content":p.script_content,
                "upload_time":str(p.upload_time),
                "script_title":p.script_title,
                "author":p.author,
                "Script_usage":p.Script_usage,
                "play_age":p.play_age.age_section,
                "play_position":p.play_position.Position_type,
                "play_sex":p.play_sex.sex_option,
                "play_actor_number":p.play_actor_number.actor_numbers,
                "play_product_option":p.play_product_option.product_options,
                "play_content":p.play_content.content_type,
                "play_script_type":p.play_script_type.script_types,
                }))
    except Exception as e:
        return render(request,"login/404.html",{"mistake":e})   
    
    
def look_all_compile(request):
    try:
        compilename=""
        if request.GET:
            compilename=request.GET["compilename"]  
        else:
            compilename=request.session.get("compilename")
        request.session["compilename"]=compilename  
        now_time=datetime.datetime.today()
        request.session["action"]="查看全部"
        request.session["now_time"]=str(now_time)
        journal(request)
        plays=play.objects.filter(Q(author=compilename) & Q(Script_usage__gt=0))
        page = request.POST.get('page')
        paginator = Paginator(plays, 3)
        try:
            rows = paginator.page(page)
        except PageNotAnInteger:
            rows = paginator.page(1)
        except EmptyPage:
            rows = paginator.page(paginator.num_pages)
        return render(request,"compile/all_plays.html",{"plays":rows})
    except Exception as e:
        return render(request,"login/404.html",{"mistake":e})   
    
    
    
    
    