from django.shortcuts import render
from app01.models import user
# Create your views here.
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from botocore.vendored.requests.api import request
def Administrator_show(request):
    username=request.GET.get("username")
    user_count=user.objects.filter(Q(name=username) & Q(role_type="Administrator")).count()
    if user_count>0:
        
        users=user.objects.filter(Q(role_type="audit") | Q(role_type="scriptwriter") | Q(role_type="actor"))
        return render(request,"Administrator/Administrator_show.html",{"users":users})
    else:
        return HttpResponse("你没有管理员权限")
from django.http import HttpResponse
import json
def Acquire_role(request):
    sc_id=request.POST.get("sc_id1")
    role=user.objects.filter(id=sc_id)
    for r in role:
        return HttpResponse(json.dumps({"status":r.role_type,"sc_id":sc_id}))  
        
from compile.models import play          
def scriptwriter_manage(request):
    plays=play.objects.all()
    paginator = Paginator(plays,3,3) 
    try: 
        num = request.GET.get('index','1') 
        number = paginator.page(num)
    except PageNotAnInteger: 
        number = paginator.page(1) 
    except EmptyPage: 
        number = paginator.page(paginator.num_pages) 
    cont={
        'page':number,
        "articles":paginator
        }
    
    return render(request,"Administrator/scriptwriter_manage.html",cont)
from artist.models import approved_memo,task
def audit_manage(request):
    sc_id=request.GET.get("id")
    role=request.GET.get("role")   
    users=user.objects.filter(Q(id=sc_id) & Q(role_type=role))
    for u in users:
        approved_memos=approved_memo.objects.filter(audit_user=u.name)
        return render(request,"Administrator/audit_manage.html",{"approved_memos":approved_memos})

def actor_manage(request):
    tasks=task.objects.all()
    paginator = Paginator(tasks,3,3) 
    try: 
        num = request.GET.get('index','1') 
        number = paginator.page(num)
    except PageNotAnInteger: 
        number = paginator.page(1) 
    except EmptyPage: 
        number = paginator.page(paginator.num_pages) 
    cont={
        'page':number,
        "articles":paginator
        }
    
    
    return render(request,"Administrator/actor_manage.html",cont)  


from app01.models import user
import datetime
def add_user(request):
    username=request.POST.get("username")
    tel=request.POST.get("tel")
    psw=request.POST.get("psw")
    role=request.POST.get("role")
    status=request.POST.get("status")
    now_time=datetime.datetime.now().strftime('%Y-%m-%d')
    users=user()
    users.name=username
    users.password=psw
    users.tel=tel
    users.role_type=role
    users.register_time=now_time
    users.user_state=status
    users.save()
    return HttpResponse(json.dumps({"status":"新增成功"}))
    
    
    
def del_user(request):
    sc_id=request.POST.get("sc_id1")  
    users=user.objects.filter(id=sc_id)
    users.delete()
    return HttpResponse(json.dumps({"status":"删除成功"}))
    
    

from .models import lan_various_img,lan_various,lan_various_category


# commodity_code color_specifications Stock_Quantity 

def get_particular(request):
    id=int(request.POST.get("id"))
    vars=lan_various_category.objects.filter(variouss_id=id)
    list1=[]
    for v in vars:
        list1.append(v.id)
        list1.append(v.commodity_code)
        list1.append(v.color_specifications)
        list1.append(v.Stock_Quantity)
    list2=[]
    for i in range(0,len(list1),4):
        list2.append(list1[i:i+4])
    print(list2)
    for v in vars:
        return HttpResponse(json.dumps({"list":list2,"status":"456",
        }
        ))

    

def get_all_img(request):
    codding=request.POST.get("codding")
    vars= lan_various.objects.filter(Design_code=codding)   
    
    print(codding)
    
    
    img_list=[] 
    for v in vars:
        vars1=lan_various_img.objects.filter(various_img_id=v.id)
        for v1 in vars1:
            img_list.append(v1.img_path)
            img_list.append(v1.img_name)
             
    list2=[]
    for i in range(0,len(img_list),2):
      
        list2.append(img_list[i:i+2])
    print(list2)
    return HttpResponse(json.dumps({
        "status":list2,
        }
        ))
import requests

import time
# 联盟商品链接上传方法
def goods_link_info(request):
    url=request.POST.get("url")
    api='http://api.vephp.com/hcapi?vekey=V00002707Y53998964' \
        '&para={}&pid=mm_628620083_962250410_109573700113&detail=1'.format(url)

    resp=requests.get(api)
    jsn_dt=resp.json()['data']
    now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    vars=lan_various()
    vars.Design_code=jsn_dt["seller_id"]
    try:

        vars.Image_path=jsn_dt["small_images"][0]
    except:
            try:
                vars.Image_path=jsn_dt["small_images"][1]
            except:
                vars.Image_path="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1571236557354&di=fa3be002891225c4143eb3531664f335&imgtype=0&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0106e858135099a84a0e282b5b62b5.jpg"

    vars.inventory =jsn_dt["volume"]
    vars.unit_price =""
    vars.Season_label=""
    vars.putaway ="已使用，请注意更新"
    vars.item_link= jsn_dt["item_url"]
    vars.zk_final_price= jsn_dt["zk_final_price"]
    vars.title  = str(jsn_dt["title"])
    vars.commission_rate =jsn_dt["commission_rate"]
    try:
            vars.coupon_info =jsn_dt["coupon_info"]
    except:
            vars.coupon_info =""
    vars.volume =jsn_dt["volume"]
    vars.create_time=now_time
    vars.status  ="联盟商品"

    vars.save()



    return HttpResponse(json.dumps({
        "status":"上传成功 ",
        }
        ))



def get_detail_info(url):
    
    api='http://api.vephp.com/hcapi?vekey=V00002707Y53998964' \
        '&para={}&pid=mm_628620083_962250410_109573700113&detail=1'.format(url)
        
        


    resp=requests.get(api)
    now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(resp)
    
    jsn_dt=resp.json()['data']

    mydata={}
    try:
        if 'coupon_info' in jsn_dt.keys():#说明有优惠卷
            mydata['zk_final_price']=jsn_dt['zk_final_price']
            mydata['title']=jsn_dt['title']
            mydata['commission_rate']=jsn_dt['commission_rate']
            mydata['coupon_info']=jsn_dt['coupon_info']
            mydata['volume'] = jsn_dt['volume']   
        else:#说明没有优惠卷
            mydata['zk_final_price'] = jsn_dt['zk_final_price']
            mydata['title'] = jsn_dt['title']
            mydata['commission_rate'] = jsn_dt['commission_rate']
            mydata['coupon_info'] = '没有优惠卷。'
            mydata['volume'] = jsn_dt['volume']
            
    except:
        return 'error'
    
    print()
    return mydata

# 仓库商品链接上传方法
def user_cargo(request):
    
    
    #这里会有脚本调用这个link ，获取折扣值等详细数据
    link=request.POST.get("link")
    now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    mydata=get_detail_info(link)
    if mydata=="error":
        return HttpResponse(json.dumps({"status":"此链接上传失败，请联系管理员",}))
    else:
        uid=request.POST.get("uid")
        
        
        vars=lan_various.objects.filter(id=uid)
        
        
        vars.update(item_link=link)
        vars.update(zk_final_price=mydata['zk_final_price'])
        vars.update(title=mydata['title'])
        vars.update(commission_rate=mydata['commission_rate'])
        vars.update(coupon_info=mydata['coupon_info'])
        vars.update(volume=mydata['volume'])
        vars.update(create_time=now_time)
        vars.update(status="仓库商品")
        

        
        
        for v in vars:
            if v.putaway=="未使用，未上传图片":
                return HttpResponse(json.dumps({
                "status":"您未上传图片，请先上传图片再使用",
                }
                ))
            else:
                
                lan_various.objects.filter(id=v.id).update(putaway="已使用，请注意更新")
                return HttpResponse(json.dumps({
                "status":"使用成功",
                }
                ))



# codding+"  "+is_putaway +"  "+ Version_state+"  "+ Season_label+"  "+ Send_time+"  "+ Version_time  +"  "+img_state

def search(request): 
    
    codding=request.POST.get("codding")
    Season_label=request.POST.get("Season_label")
    img_state=request.POST.get("img_state")
    try:
        if codding:
            request.session["codding"]=codding
        else:
            del request.session["codding"]
        return HttpResponse(json.dumps({
                "status":"使用成功",
                }
                )) 
    except:
        if Season_label:
            request.session["Season_label"]=Season_label
            request.session["img_state"]=img_state
            if request.session["img_state"]=="00":
                del request.session["img_state"]
            if request.session["Season_label"]=="00":
                del request.session["Season_label"]
   
        else:
            del request.session["Season_label"]
        
    
        return HttpResponse(json.dumps({
                "status":"使用成功",
                }
                )) 






def del_picture(request):
    path=request.POST.get("path")
    print(path)
    

    lans=lan_various_img.objects.filter(img_path=path)
    for i in lans:
        print("当前货品id",i.various_img_id)
        lans_list=lan_various_img.objects.filter(various_img_id=i.various_img_id)
        lan_various_img.objects.filter(img_path=path).delete()
        for l in lans_list:
            lan_various.objects.filter(id=i.various_img_id).update(Image_path=l.img_path)
            print(l.img_path)

#     lan_various_img.objects.filter(img_path=path).delete()
    return HttpResponse(json.dumps({
                "status":"删除成功"
                }
                ))  

from Administrator.models import order
def look_manifest(request):
    
    users=user.objects.filter(role_type="microblog_user")
    
    
    return render(request,"Administrator/look_manifest.html",{"users":users})

# tk_paid_time   pub_share_fee pub_share_pre_fee  alipay_total_price  item_num adzone_name
from .models import tbaok_anzone
def get_lnnkj(request):

    if request.method == 'GET':
        page = request.GET.get('page')
        num = request.GET.get('rows')
        right_boundary = int(page)*int(num)
        if request.GET.get("search_kw"):
            page_user = order.objects.filter(Q(id__gt=0) & Q(adzone_name=request.GET.get("search_kw"))).order_by("-tk_paid_time")[int(num)*(int(page)-1):right_boundary]
            total = order.objects.filter(Q(id__gt=0) & Q(adzone_name=request.GET.get("search_kw"))).order_by("-tk_paid_time").count()
        else:
            page_user = order.objects.filter(id__gt=0).order_by("-tk_paid_time")[int(num)*(int(page)-1):right_boundary]
            total = order.objects.filter(id__gt=0).order_by("-tk_paid_time").count()
        rows = []
        for user in page_user:
            tbaoks=tbaok_anzone.objects.filter(adzone_name=user.adzone_name)
            for t in tbaoks:
                user_name=t.user_name
            rows.append({'id':user.id,'tk_paid_time': user.tk_paid_time, 'pub_share_fee':user.pub_share_fee , 'pub_share_pre_fee':user.pub_share_pre_fee,"alipay_total_price":user.alipay_total_price,"item_num":user.item_num,"adzone_name":user.adzone_name,"item_title":user.item_title,"good_url":"<a href="+user.item_link+" target='_blank'>"+user.item_link+"</a>"})                                          
        return HttpResponse(json.dumps({'total': total, 'rows': rows}))
        

def get_good_particulars(request):
    
    print("进来了")
    if request.method == 'GET':
        search_kw = request.GET.get('search_kw', None)
        page = request.GET.get('page')
        num = request.GET.get('rows')
        right_boundary = int(page)*int(num)
        
        if search_kw:
            page_user = lan_various.objects.filter(id__gt=0)
            total = lan_various.objects.filter(id__gt=0).count()
        else:
            page_user = lan_various.objects.filter(Q(id__gt=0) & Q(putaway='已使用，请注意更新')  ).order_by("-create_time")[int(num)*(int(page)-1):right_boundary]
            total = lan_various.objects.filter(Q(id__gt=0) & Q(putaway='已使用，请注意更新')).count()
        rows = []
        for user in page_user:            
            Design_code="<span style='font-size:2px'>库存量：</span><br><strong style='color:#FC7903;'>"+str(user.inventory)+"</strong><br><span>季节标签:</span><br><strong style='color:#008000'>"+user.Season_label+"</strong><br><a   target='_blank' id='link'  href='"+user.item_link+"'>查看商品详情</a>"
            commission="<span >产品折后价 ：</span><br><strong style='color:#FC7903;'>"+str(user.zk_final_price)+"</strong><br><span>商品标题:</span><br><strong style='color:#008000'>"+str(user.title)+"</strong><br><span>佣金比例:</span><br><strong style='color:#008000'>"+str(user.commission_rate)+"（百分比）</strong><br> <span>优惠卷信息:</span><br><strong style='color:#008000'>"+str(user.coupon_info)+"</strong><br> <span>近30天销量:</span><br><strong style='color:#008000'>"+str(user.volume)+"</strong>"
            path_url=user.Image_path 
            
            path3=user.Image_path.split('/')[3]
            
            
            
            id="<a  href='javascript:;' onclick=\"cheak_img('" + path3 + "', view='view')\" title='查看' ><img  style='width: 200px;height:200px' src="+path_url+"></a><br>"+user.Design_code
            rows.append({'sid':user.id,'id': id, 'name':Design_code , 'is_delete':user.putaway,"commission":commission})
        return HttpResponse(json.dumps({'total': total, 'rows': rows}))
    

#删除商品
def del_goods(request):
    del_id=request.POST.get("del_id")
    
    
    lans=lan_various.objects.filter(id=del_id)
    try:
        lans.delete()
        status="删除成功"
    except:
        status="删除失败"
    return HttpResponse(json.dumps({'status': status}))


from django.http import HttpResponseRedirect
import os      
from lanlanTest21.settings import STATICFILES_DIRS
# 仓库商品图片上传        
def goods_picture_upload(request): 
    id=request.POST.get("id")
    
    print("6666",id)
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
            
            return HttpResponseRedirect("Goods_upload")    
    except:
        
        message="请选择图片"
        request.session["message"]=message
        
        return HttpResponse("请选择图片")


def describe_upload(request):
    sid=request.POST.get("id")
    describe=request.POST.get("describe")
    
    lan_various.objects.filter(id=sid).update(product_description=describe)
    return HttpResponseRedirect("Goods_upload") 
    
    
    
from Administrator.models import goods_video   
def task_upload(request):
    
    
    print("商品视频进来了")
    try:
        f1 = request.FILES.get('video')
        uploadid=request.POST.get("id")

        p = goods_video()
        p.video_title=uploadid
        p.video_path="/goods_video/%s/"%uploadid + f1.name
        p.video_goods_id=uploadid
        p.save()
        try:
            fname = str(STATICFILES_DIRS[0]) + "/goods_video/%s/"%uploadid + f1.name
            with open(fname,'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
        except:
            os.makedirs(str(STATICFILES_DIRS[0]) + "/goods_video/%s/"%uploadid) 
            fname = str(STATICFILES_DIRS[0]) + "/goods_video/%s/"%uploadid + f1.name
            with open(fname,'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)

        
        return HttpResponseRedirect("Goods_upload") 
    except:
       
        return  HttpResponse("请选择文件<a href='/Goods_upload'>返回页面</a>")
    
    
    
    
def abc(request):
    
    
    return render(request,"Administrator/abc.html")    
    
def get_secondary(request):
    second_person=request.POST.get("clothing")
    print(second_person)
    tbs_list=tbaok_anzone.objects.filter(user_name=second_person)
    tbsa_list=[]
    for t in tbs_list:
        print(t.adzone_name)
        tbsa_list.append(t.adzone_name)
    return HttpResponse(json.dumps({"result":tbsa_list}))

    
    
    
    
    
    
    
    
    
    
      

    