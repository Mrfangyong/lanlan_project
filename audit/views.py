from django.shortcuts import render,redirect
from artist.models import task,approved_memo,video
from django.http import HttpResponse
import datetime
from app01.models import journal1

def journal(request):
    compilename=request.session.get("username")
    action=request.session.get("action")
    time=request.session.get("now_time")
    jour=journal1(journal_name=compilename,journal_action=action,journal_time=time)
    jour.save()


def audit_show(request):
    username=""
    if request.GET:
        username=request.GET["username"]
    else:
        username=request.session.get("username")
    if request.session.get("status1"):
        request.session["username"]=username
        username=request.GET.get("username")
        
        now_time=datetime.datetime.today()
        request.session["action"]="审核登陆"
        request.session["now_time"]=str(now_time)
        journal(request)
        
        tasks=task.objects.filter(task_status="成功提交视频，等待审核")
        return render(request,"audit/audit_index.html",{"tasks":tasks})
    else:
        return redirect("/index")




import json
def cheakvideo(request):
    video_id=request.POST.get("sc_id1")
    videos=video.objects.filter(id=video_id)
    for v in videos:
        return HttpResponse(json.dumps({"videos": str(v.video_path)})) 
    
    
    
    
def pass_the_audit(request):
    task_id=request.POST.get("sc_id1")
    now_time=datetime.datetime.now().strftime('%Y-%m-%d')
    username=request.session.get("username")
    task.objects.filter(id=task_id).update(task_status="审核通过")
    app=approved_memo()
    app.tid_id=task_id
    app.audit_time=now_time
    app.audit_user=username
    app.save()
    
    status="操作成功"
    
    now_time=datetime.datetime.today()
    request.session["action"]=task_id+"审核通过"
    request.session["now_time"]=str(now_time)
    journal(request)
    
    return HttpResponse(json.dumps({"status":status})) 
    
def Not_approved(request):
    task_id=request.POST.get("sc_id1")
    cause=request.POST.get("cause")
    now_time=datetime.datetime.now().strftime('%Y-%m-%d')
    username=request.session.get("username")
    
    task.objects.filter(id=task_id).update(task_status="审核不通过，理由：%s"%cause)
    app=approved_memo()
    app.tid_id=task_id
    app.audit_time=now_time
    app.audit_user=username
    app.save()
    status="操作成功"
    
    now_time=datetime.datetime.today()
    request.session["action"]=task_id+"审核不通过，理由：%s"%cause
    request.session["now_time"]=str(now_time)
    journal(request)
    
    return HttpResponse(json.dumps({"status":status})) 
    
    
def cheakaduit(request):
    username=request.session.get("username")
    approved_memos=approved_memo.objects.filter(audit_user=username)
    return render(request,"audit/cheakaduit.html",{"approved_memos":approved_memos})   
def withdraw(request):
    task_id=request.POST.get("sc_id1")
    approved_memos=approved_memo.objects.filter(id=task_id)
    for a in approved_memos:
        task.objects.filter(id=a.tid_id).update(task_status="成功提交视频，等待审核")
    deletesql = approved_memo.objects.filter(id=task_id)  # 执行删除操作
    deletesql.delete()
    status="操作成功"
    
    now_time=datetime.datetime.today()
    request.session["action"]=task_id+"撤回审核操作"
    request.session["now_time"]=str(now_time)
    journal(request)
    
    return HttpResponse(json.dumps({"status":status})) 
    
    
    