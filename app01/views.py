from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,render_to_response
from compile.models import age,position,sex,actor_number,product_option,content,script_type,play
# Create your views here.
from django.http import HttpResponse
from lanlanTest21.settings import STATICFILES_DIRS
from app01.models import user
import json
def app01_index(request):
    return render(request,"login/index.html")
def login_username(request):
    try:
        
        state=True
        char="@#$%^&*(){}!|<>?"
        username=request.POST.get("username")
        
        
        
        
        for c in char:
                if c in username:
                    state=False
                if state==False:
                    message="用户名包含特殊字符，请检查！！！"
                    return HttpResponse(json.dumps({"status":message}))
        
#         登陆主放到session中去
        request.session["username"]=username
        print("这个人进来了",username)
        password=request.POST.get("password")
        user1=user.objects.filter(name=username)
        if user1.count()>0:
            for i in user1:
                if i.password==password:
                    if i.role_type=="actor":
                        request.session["status1"]=True
                        return HttpResponse(json.dumps({"status":"演员登陆成功","role":"actor"}))
                    elif i.role_type=="scriptwriter":
                        request.session["status1"]=True
                        return HttpResponse(json.dumps({"status":"编剧登陆成功","role":"scriptwriter"}))
                    elif i.role_type=="Administrator":
                        request.session["status1"]=True
                        return HttpResponse(json.dumps({"status":"管理员登陆成功","role":"Administrator"}))
                    elif i.role_type=="audit":
                        request.session["status1"]=True
                        return HttpResponse(json.dumps({"status":"审核登陆成功","role":"audit"}))
                    elif i.role_type=="microblog_user":
                        request.session["status1"]=True
                        return HttpResponse(json.dumps({"status":"登陆成功","role":"microblog_user"}))
                else:
                    return HttpResponse(json.dumps({"status":"密码不正确"}))
        else:
            return HttpResponse(json.dumps({"status":"姓名不存在"}))
    except:
        return HttpResponse(json.dumps({"status":"姓名不存在"}))
def  Get_task(request):
    ages=age.objects.all()
    positions=position.objects.all()
    sexs=sex.objects.all()
    actor_numbers=actor_number.objects.all()
    product_options=product_option.objects.all()
    contents=content.objects.all()
    script_types=script_type.objects.all()
    plays=play.objects.all()
    paginator = Paginator(plays,10,3) 
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
    return render(request,"artist/Get_task.html",dict1)
def  Artist_ranking(request):
    return render(request,"artist/Artist_ranking.html")
def  sample_video(request):
    return render(request,"artist/sample_video.html")
def Upload_script(request):
    ages=age.objects.all()
    positions=position.objects.all()
    sexs=sex.objects.all()
    actor_numbers=actor_number.objects.all()
    product_options=product_option.objects.all()
    contents=content.objects.all()
    script_types=script_type.objects.all()
    dict1={
        "ages":ages,
        "positions":positions,
        "sexs":sexs,
        "actor_numbers":actor_numbers,
        "product_options":product_options,
        "contents":contents,
        "script_types":script_types,
        }
    return render(request,"compile/Upload_script.html",dict1)   
def script_ranking(request):
    return render(request,"compile/script_ranking.html")
def Outstanding_drama(request):
    return render(request,"compile/Outstanding_drama.html")




from Administrator.models import tbaok_anzone,links_convert,order

# 测试方法
def test1(request):
    username="libaomin"
    tbs=tbaok_anzone.objects.filter(user_name=username)
    tbs_list=[]
    for i in tbs:
        print(i.adzone_ids)
        tbs_list.append(i.adzone_ids)
     
    return HttpResponse(tbs)





def page_not_found(request):
    return render_to_response('login/404.html')


from app01.models import mistake as mistake_end
import datetime
def mistake(request):
    mistake1=request.POST.get("mistake")
    today=datetime.datetime.today()
    mistakes=mistake_end(mistake_content=str(mistake1),mistake_time=today)
    mistakes.save()
    return HttpResponse(json.dumps({"status":"暂时返回主页，等待管理员处理"}))

from app01.models import Student

# 重中之重
# def xuni(request):
#     
#     
#     
#     students=Student.a_m.all()
#     print("1236465",request.META.get("REMOTE_ADDR"))
#     for s in students:
#         print(s.name)
#     for key in request.META:
#         return HttpResponse(key,request.META.get(key))
#     



def bootstrapTable(request):
    return render(request,"Administrator/ceshi.html")
def sss(request):
    list1=[]
    stus=Student.objects.all()
    for s in stus:
        list1.append({"id": s.id,"name": s.name,"is_delete": s.is_delete,})
    datalist = {
        "total": 1,
        "rows":list1
    }
    return HttpResponse(json.dumps(datalist))

from django.db.models import Q
from Administrator.models import lan_various,lan_various_category,lan_various_img

    
def getdata1(request):
    from botocore.vendored.requests.compat import str
    if request.method == 'GET':
        search_kw = request.GET.get('search_kw', None)
        page = request.GET.get('page')
        
        
        num = request.GET.get('rows')
        right_boundary = int(page)*int(num)
        
        print("当前页",page)
        print(num)
        print(right_boundary)
#         del request.session["Version_state"]
        if search_kw:
            page_user = lan_various.objects.filter(id__gt=0)
            total = lan_various.objects.filter(id__gt=0).count()
        else:
            if request.session.get("codding"):
                page_user = lan_various.objects.filter(Q(id__gt=0) & Q(Design_code__contains=request.session.get("codding")))[int(num)*(int(page)-1):right_boundary]
                total = lan_various.objects.filter(Q(id__gt=0) & Q(Design_code=request.session.get("codding"))).count()
            elif request.session.get("img_state") and request.session.get("Season_label"):
                page_user = lan_various.objects.filter(Q(id__gt=0) & Q(putaway=request.session.get("img_state")) & Q(Season_label__contains=request.session.get("Season_label")))[int(num)*(int(page)-1):right_boundary]
                total = lan_various.objects.filter(Q(id__gt=0) & Q(putaway=request.session.get("img_state")) & Q(Season_label__contains=request.session.get("Season_label"))).count()
            elif request.session.get("Season_label"):
                if request.session.get("img_state"):
                    print("有状态",request.session.get("img_state"))
                else:
                    print("无状态",request.session.get("img_state"))
                page_user = lan_various.objects.filter(Q(id__gt=0) & Q(Season_label__contains=request.session.get("Season_label")))[int(num)*(int(page)-1):right_boundary]
                total = lan_various.objects.filter(Q(id__gt=0) & Q(Season_label__contains=request.session.get("Season_label"))).count()                
            elif request.session.get("img_state"):
                page_user = lan_various.objects.filter(Q(id__gt=0) & Q(putaway=request.session.get("img_state")))[int(num)*(int(page)-1):right_boundary]
                total = lan_various.objects.filter(Q(id__gt=0) & Q(putaway=request.session.get("img_state"))).count()
            else:
                page_user = lan_various.objects.filter(id__gt=0)[int(num)*(int(page)-1):right_boundary]
                total = lan_various.objects.filter(id__gt=0).count()
        rows = []
        for user in page_user:
            Design_code="<span style='font-size:2px'>库存量：</span><br><strong style='color:#FC7903;'>"+str(user.inventory)+"</strong><br><span>季节标签:</span><br><strong style='color:#008000'>"+user.Season_label+"</strong><br>"
            path_url=user.Image_path 
            path3=user.Image_path.split('/')[3]
            
            
            
            id="<a href='javascript:;' onclick=\"cheak_img('" + path3 + "', view='view')\" title='查看' ><img  style='width: 200px;height:200px' src="+path_url+"></a><br>"+user.Design_code
            rows.append({'sid':user.id,'id': id,'unit_price': str(user.unit_price)+"元",'name':Design_code , 'is_delete':user.putaway})
        return HttpResponse(json.dumps({'total': total, 'rows': rows}))
    
    
# 图片上传   之前是获取的id  经过id 获取款式码
from django.http import HttpResponseRedirect
import os
def picture_upload(request):
    id=request.POST.get("id")
    try:
        content =request.FILES.get("picture")
        vars=lan_various.objects.filter(id=id)
        
        
        for v in vars:
            var=lan_various_img()
            var.img_name=content.name
            var.img_path="/static/Commodity_images/%s/"%v.Design_code + content.name
            var.various_img_id=id
            var.save()
            try:
                fname = str(STATICFILES_DIRS[0]) + "/Commodity_images/%s/"%v.Design_code + content.name
                with open(fname,'wb') as pic:
                    for c in content.chunks():
                        pic.write(c)
            except:
                os.makedirs(str(STATICFILES_DIRS[0]) + "/Commodity_images/%s/"%v.Design_code ) 
                fname = str(STATICFILES_DIRS[0]) +  "/Commodity_images/%s/"%v.Design_code + content.name
                with open(fname,'wb') as pic:
                    for c in content.chunks():
                        pic.write(c)
                        
                        
            if v.putaway=="已使用，请注意更新":
                lan_various.objects.filter(id=v.id).update(putaway="已使用，请注意更新")
            else:  
                lan_various.objects.filter(id=v.id).update(putaway="款式未使用，图片已上传")
            lan_various.objects.filter(id=v.id).update(Image_path=var.img_path)
            
            return HttpResponseRedirect("bootstrapTable")    
    except:
        
        message="请选择图片"
        request.session["message"]=message
        
        return HttpResponse("请选择图片")
    
    
    
    
    
    
    
