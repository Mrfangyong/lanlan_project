import json
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from Administrator.models import tbaok_anzone,links_convert,order
# Create your views here.
from app01.models import user



def microblog_user_show(request):
    
    
#     推过记录   我的订单详情数据  切换   
#     我的订单详细数据  item_title  item_num site_name   pub_share_fee  pay_price  
#     推广记录  时间，推广商品链接 （跳）  生成的链接（三个）

# https://www.cnblogs.com/gcgc/p/11162164.html    
    
    
    username=request.session.get("username")
    name=request.GET.get("username")
    if name==None:
        name=request.POST.get("username")
    if request.session.get("username")==None:
        request.session["username"]=request.GET.get("username")
    
    
    if request.session.get("username")==None:
        username=request.POST.get("username")
    
    if request.session.get("status1")==None:
        return HttpResponseRedirect("/")



    links=links_convert.objects.filter(user_name=username)
    page1 = request.POST.get('page1')
    paginator1 = Paginator(links, 3)
    try:
        rows1 = paginator1.page(page1)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        rows1 = paginator1.page(1)
    except EmptyPage:
        rows1 = paginator1.page(paginator1.num_pages)



    tbs=tbaok_anzone.objects.filter(user_name=name)
    tbs_list=[]
    
    for i in tbs:
        tbs_list.append(i.adzone_name)
    
    print(tbs_list)
    orders=order.objects.filter(adzone_name__in=tbs_list)
    page = request.POST.get('page')
    paginator = Paginator(orders, 3)
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        rows = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        rows = paginator.page(paginator.num_pages)

    return render(request,"microblog/new_index.html",{"username":name,"rows":rows,"rows1":rows1})
#本人详细数据
def Order_details(request):
    session_username=request.session.get("username")
    generalize_list=[]
    tbaok_anzones=tbaok_anzone.objects.filter(user_name=session_username)
    for t in tbaok_anzones:
        generalize_list.append(t.account_name)
    print("所有的推广位",generalize_list)
    if request.method == 'GET':
        page = request.GET.get('page')
        num = request.GET.get('rows')
        right_boundary = int(page)*int(num)
        page_user = order.objects.filter(adzone_name__in=generalize_list).order_by("-id")[int(num)*(int(page)-1):right_boundary]
        total = order.objects.filter(adzone_name__in=generalize_list).count()
        print("所有的个数",total)
        rows = []
        for user in page_user:
            rows.append({"id":user.id,"good_title":user.item_title,"good_num":user.item_num,"Promotion_name":user.adzone_name
                         ,"Estimated_income":user.pub_share_pre_fee,"payment_amount":user.alipay_total_price,"order_time":user.tb_paid_time})
        return HttpResponse(json.dumps({'total': total, 'rows': rows}))

def Generalize_product(request):
    session_username=request.session.get("username")

    if request.method == 'GET':
        page = request.GET.get('page')
        num = request.GET.get('rows')
        right_boundary = int(page)*int(num)
        page_user = links_convert.objects.filter(user_name=session_username).order_by("-request_time")[int(num)*(int(page)-1):right_boundary]
        total = links_convert.objects.filter(user_name=session_username).count()
        print(total)      
        rows = []
            
        for user in page_user:            
            rows.append({"id":user.id,"Promotion_time":user.request_time,"Product_link":"<a href="+user.my_tb_link+" target='_blank'>"+user.my_tb_link+"</a>",
                         "two_in_one_links":"<a  href="+user.coupon_click_url+" target='_blank'>"+user.coupon_click_url+"</a>",
                         "tbk_pwd":user.tbk_pwd,
                         "coupon_short_url":"<a  href="+user.coupon_short_url+" target='_blank'>"+user.coupon_short_url+"</a>"})
        return HttpResponse(json.dumps({'total': total, 'rows': rows}))
    


def choose_product(request):
#     去查已经上过淘宝店的货
    
   
    username=request.GET.get("username")
    if username==None:
        username=request.session.get("username")
    tbaok_anzones=tbaok_anzone.objects.filter(Q(user_name=username) & Q(status=1))
    return render(request,"microblog/Taobao_product.html",{"username":username,"tbaok_anzones":tbaok_anzones})
    



def add_platform_user(request):
    platform_name=request.POST.get("username")
    account_name=request.POST.get("platform")
    tbaoks=tbaok_anzone()
    tbaoks.user_name=request.session.get("username")
    tbaoks.platform=platform_name
    tbaoks.account_name=account_name
    tbaoks.status=0
    tbaoks.save()
    return HttpResponse(json.dumps({"status":"新增成功,平台正在审核，预计审核时间一天"}))
from django.db.models import Q    
from Administrator.models import lan_various,lan_various_category,lan_various_img

def get_already_have(request):
    if request.method == 'GET':
        search_kw = request.GET.get('search_kw', None)
        page = request.GET.get('page')
        num = request.GET.get('rows')
        
        print("当前页",page)
        print("页数",num)
        
        right_boundary = int(page)*int(num)
        
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
                page_user = lan_various.objects.filter(Q(id__gt=0) & Q(putaway='已使用，请注意更新')  ).order_by("-create_time")[int(num)*(int(page)-1):right_boundary]
                total = lan_various.objects.filter(Q(id__gt=0) & Q(putaway='已使用，请注意更新')).count()
                
                
                print("所有的个数",total)
                
        rows = []
        for user in page_user:            
            Design_code="<span style='font-size:2px'>库存量：</span><br><strong style='color:#FC7903;'>"+str(user.inventory)+"</strong><br><span>季节标签:</span><br><strong style='color:#008000'>"+user.Season_label+"</strong><br><a   target='_blank' id='link'  href='"+user.item_link+"'>查看商品详情</a>"
            commission="<span >产品折后价 ：</span><br><strong style='color:#FC7903;'>"+str(user.zk_final_price)+"</strong><br><span>商品标题:</span><br><strong style='color:#008000'>"+str(user.title)+"</strong><br><span>佣金比例:</span><br><strong style='color:#008000'>"+str(user.commission_rate)+"（百分比）</strong><br> <span>优惠卷信息:</span><br><strong style='color:#008000'>"+str(user.coupon_info)+"</strong><br> <span>近30天销量:</span><br><strong style='color:#008000'>"+str(user.volume)+"</strong>"
            path_url=user.Image_path 
            
            path3=user.Image_path.split('/')[3]
            print(path3)
            id="<a  href='javascript:;' onclick=\"cheak_img('" + path3 + "', view='view')\" title='查看' ><img  style='width: 200px;height:200px' src="+path_url+"></a><br>"+user.Design_code
            rows.append({'sid':user.id,'id': id, 'name':Design_code , 'is_delete':user.putaway,"commission":commission})
        return HttpResponse(json.dumps({'total': total, 'rows': rows}))
    
        #                 path3=user.Image_path.split('/')[3]

from django.db import connection
import requests
import MySQLdb
def insert_data(data_table,data_dict):
    
    db = MySQLdb.connect("localhost", "root", "123", "ajax_base", charset='utf8' )
    cursor = db.cursor()
    placeholders = ', '.join(['%s'] * len(data_dict))
    columns = ', '.join(data_dict.keys())

    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (data_table, columns, placeholders)

    datas =  tuple(data_dict.values())
    cursor.execute(sql, datas)
    db.commit()
#    category_id coupon_click_url coupon_end_time coupon_info coupon_remain_count coupon_start_time coupon_total_count coupon_type
#    commission_rate num_iid tbk_pwd coupon_short_url request_time user_name my_tb_link adzone_id

def link_convert(request_time,user_name,my_tb_link,anzone_id):
    api2='http://api.vephp.com/hcapi?vekey=V00002707Y53998964&para={}&pid={}'.format(my_tb_link,anzone_id)
    resp2=requests.get(api2)
    myitem_info=resp2.json()['data']
    myitem_info['request_time']=request_time
    myitem_info['user_name']=user_name
    myitem_info['my_tb_link']=my_tb_link
    myitem_info['anzone_id']=anzone_id
    
    print(myitem_info)
    
    links=links_convert()
    links.adzone_id=anzone_id
    links.category_id=myitem_info['category_id']
    links.commission_rate=myitem_info['commission_rate']
    links.coupon_click_url=myitem_info['coupon_click_url']
    try:
        links.coupon_end_time=myitem_info['coupon_end_time']
        links.coupon_info=myitem_info['coupon_info']
        links.coupon_remain_count=myitem_info['coupon_remain_count']
        links.coupon_short_url=myitem_info['coupon_short_url']
        links.coupon_start_time=myitem_info['coupon_start_time']
        links.coupon_total_count=myitem_info['coupon_total_count']
        links.coupon_type=myitem_info['coupon_type']
    except:
        links.coupon_end_time=""
        links.coupon_info=""
        links.coupon_remain_count=""
        links.coupon_short_url=""
        links.coupon_start_time=""
        links.coupon_total_count=""
        links.coupon_type=""
    links.my_tb_link=myitem_info['my_tb_link']
    links.num_iid=myitem_info['num_iid']
    links.tbk_pwd=myitem_info['tbk_pwd']
    links.user_name=myitem_info['user_name']
    links.my_tb_link=myitem_info['my_tb_link']
    links.request_time=myitem_info['request_time']
    links.save()

#     insert_data('administrator_links_convert',myitem_info) 
    return myitem_info["coupon_click_url"],myitem_info["tbk_pwd"],myitem_info["coupon_short_url"]
from datetime import datetime
now_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_exclusive_links(request):

    exclusive =request.POST.get("exclusive")
    link =request.POST.get("link")
    link_list=exclusive.split(" ")
    request_time=now_time
    user_name=request.session.get("username")
    my_tb_link=link
    
    
    anzone_id123=link_list[1]
    print(link)
    print(anzone_id123)
    
    linkss=links_convert.objects.filter(Q(user_name=user_name) & Q(my_tb_link=my_tb_link) &Q(adzone_id=anzone_id123))
    if linkss.count()>0:
        for i in linkss:    
            return HttpResponse(json.dumps({'coupon_click_url':i.coupon_click_url,'tbk_pwd':i.tbk_pwd,"coupon_short_url":i.coupon_short_url}))
    else:
        coupon_click_url,tbk_pwd,coupon_short_url=link_convert(request_time,user_name,my_tb_link,anzone_id123)
        return HttpResponse(json.dumps({'coupon_click_url':coupon_click_url,'tbk_pwd':tbk_pwd,"coupon_short_url":coupon_short_url}))

def get_already_link(request):
    link=request.POST.get("link")
    links=links_convert.objects.filter(my_tb_link=link)
    for l in links:       
        return HttpResponse(json.dumps({'coupon_click_url':l.coupon_click_url,"tbk_pwd":l.tbk_pwd,"coupon_short_url":l.coupon_short_url}))
    
    
    
def get_promotion(request):
    username=request.POST.get("username")
    tbaoks=tbaok_anzone.objects.filter(user_name=username)
    list1=[]
    for v in tbaoks:
        list1.append(v.adzone_name)
        list1.append(v.adzone_id)
        list1.append(v.account_name)
        
        if v.status=="1":
            list1.append("审核通过")
        else:
            list1.append("审核中....")
    list2=[]
    for i in range(0,len(list1),4):
        list2.append(list1[i:i+4])
    print(list2)
    return HttpResponse(json.dumps({"tbaoks":list2}))
    


    
def search(request):
    seach1=request.POST.get("seach1")
    
    print("搜索词")
    if seach1:
        request.session["seach1"]=seach1
    else:
        del request.session["seach1"]
    return HttpResponse(json.dumps({
            "status":"使用成功",
            }
            )) 

    

# 联盟商品链接上传
def Goods_upload(request):
    return render(request,"microblog/Goods_upload.html")
    
    
    
    
    
    
    
#     大淘客
#     获取推广位 
def Transition_zone(request):
    username=request.GET.get("username")
    if username==None:
        username=request.session.get("username")
    tbaok_anzones=tbaok_anzone.objects.filter(Q(user_name=username) & Q(status=1))
    return render(request,"microblog/Transition_zone.html",{"username":username,"tbaok_anzones":tbaok_anzones})
    
from microblog.dataoke import action,to_short2
def guest_links(request):
    exclusive=request.POST.get("exclusive")
    good_id=request.POST.get("good_id")
    goods_info=action(exclusive.split(" ")[1],good_id)
    return HttpResponse(json.dumps({"status":goods_info}))
    
    
def Double_Eleven(request):

    username=request.GET.get("username")
    if username==None:
        username=request.session.get("username")
    tbaok_anzones=tbaok_anzone.objects.filter(Q(user_name=username) & Q(status=1))
    return render(request,"microblog/Double_Eleven.html",{"username":username,"tbaok_anzones":tbaok_anzones})




1
from microblog.double_eleven import get_shuangshiyi 

def get_double_eleven(request):
    
    exclusive=request.POST.get("exclusive")
    category=request.POST.get("category")


    if exclusive==None:
        exclusive=request.session.get("exclusive")

    if category==None:
        category=request.session.get("category")

    request.session["exclusive"]=exclusive
    request.session["category"]=category


#         rows=category_all_goods["data"]
    rows=[]


    category_all_goods=get_shuangshiyi(category,exclusive.split(" ")[1],1)

    for i in range(len(category_all_goods["data"])):
        pict_url="<img style='width:200px;height:200px' src="+category_all_goods["data"][i]['pict_url']+">"
        click_url="<a target='_blank' href="+category_all_goods["data"][i]['click_url']+">商品详情</a>"
        commission_rate=category_all_goods["data"][i]['commission_rate'] if 'commission_rate' in category_all_goods["data"][i].keys() else ""
        coupon_amount=category_all_goods["data"][i]['coupon_amount'] if 'coupon_amount' in category_all_goods["data"][i].keys() else ""
        item_description= category_all_goods["data"][i]['item_description'] if 'item_description' in category_all_goods["data"][i].keys() else ""
        nick=category_all_goods["data"][i]['nick'] if 'nick' in category_all_goods["data"][i].keys() else ""
        presale_discount_fee_text=category_all_goods["data"][i]['presale_discount_fee_text'] if 'presale_discount_fee_text' in category_all_goods["data"][i].keys() else ""
        small_images= category_all_goods["data"][i]['item_id'] if 'item_id' in category_all_goods["data"][i].keys() else ""
        title=category_all_goods["data"][i]['title'] if 'title' in category_all_goods["data"][i].keys() else ""
        volume=category_all_goods["data"][i]['volume'] if 'volume' in category_all_goods["data"][i].keys() else ""
        zk_final_price=category_all_goods["data"][i]['zk_final_price'] if 'zk_final_price' in category_all_goods["data"][i].keys() else ""
        rows.append({"click_url":click_url,"commission_rate":commission_rate,
                       "coupon_amount":coupon_amount,
                       "item_description":item_description,
                       "nick":nick,
                       "pict_url":pict_url,
                       "presale_discount_fee_text":presale_discount_fee_text,
                       "small_images":small_images,
                       "title":title,
                       "volume":volume,
                       "zk_final_price":zk_final_price,

                       })
    total=len(category_all_goods["data"])
    print(total)
    return HttpResponse(json.dumps({'total': total, 'rows': rows}))



def Eleven_Double(request):
    username=request.GET.get("username")
    if username==None:
        username=request.session.get("username")
    tbaok_anzones=tbaok_anzone.objects.filter(Q(user_name=username) & Q(status=1))
    return render(request,"microblog/Eleven_Double.html",{"username":username,"tbaok_anzones":tbaok_anzones})


import time

def time_stamp(timeStamp):
    try:
        

        timeStamp = float(int(timeStamp)/1000) 
        timeArray = time.localtime(timeStamp) 
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray) 
        return  otherStyleTime
    except:
        return ""



    
def get_double_eleven1(request):

    exclusive=request.POST.get("exclusive")
    category=request.POST.get("category")
    new_page=request.POST.get("new_page")
    if new_page==None:
        new_page=1
    print("当前页",new_page)
    list1=[]
    category_all_goods=get_shuangshiyi(category,exclusive.split(" ")[1],new_page)
    
#  category_all_goods["data"][i]['coupon_amount'] if 'coupon_amount' in category_all_goods["data"][i].keys() else ""   
    
    
    
#commission="<span >产品折后价 ：</span><br><strong style='color:#FC7903;'>"+str(user.zk_final_price)+"</strong><br><span>商品标题:</span><br><strong style='color:#008000'>"+str(user.title)+"</strong><br><span>佣金比例:</span><br><strong style='color:#008000'>"+str(user.commission_rate)+"（百分比）</strong><br> <span>优惠卷信息:</span><br><strong style='color:#008000'>"+str(user.coupon_info)+"</strong><br> <span>近30天销量:</span><br><strong style='color:#008000'>"+str(user.volume)+"</strong>"

    print(len(category_all_goods["data"]))
    for i in range(len(category_all_goods["data"])):
        pict_url="<img style='width:200px;height:200px' src="+category_all_goods["data"][i]['pict_url']+">"
        click_url="<a target='_blank' href="+category_all_goods["data"][i]['click_url']+">商品详情</a>"
        commission_rate=category_all_goods["data"][i]['commission_rate'] if 'commission_rate' in category_all_goods["data"][i].keys() else ""
        coupon_amount="<span>优惠券（元）</span><br><strong style='color:#FC7903;'>"+str(category_all_goods["data"][i]['coupon_amount'])+"</strong><br><span>优惠券信息-优惠券结束时间</span><br><strong style='color:#FC7903;'>"+str(time_stamp(category_all_goods["data"][i]['coupon_end_time']))+"</strong><br><span>优惠券信息-优惠券剩余量</span><br><strong style='color:#FC7903;'>"+str(category_all_goods["data"][i]['coupon_remain_count'])+"</strong><br><span>优惠券信息-优惠券起用门槛，满X元可用。</span><br><strong style='color:#FC7903;'>"+str(category_all_goods["data"][i]['coupon_start_fee'])+"</strong><br><span>优惠券信息-优惠券开始时间</span><br><strong style='color:#FC7903;'>"+str(time_stamp(category_all_goods["data"][i]['coupon_start_time']))+"</strong><br>"
        item_description= category_all_goods["data"][i]['item_description'] if 'item_description' in category_all_goods["data"][i].keys() else ""
        nick=category_all_goods["data"][i]['nick'] if 'nick' in category_all_goods["data"][i].keys() else ""
        presale_discount_fee_text=category_all_goods["data"][i]['presale_discount_fee_text'] if 'presale_discount_fee_text' in category_all_goods["data"][i].keys() else ""
        small_images= category_all_goods["data"][i]['item_id'] if 'item_id' in category_all_goods["data"][i].keys() else ""
        title=category_all_goods["data"][i]['title'] if 'title' in category_all_goods["data"][i].keys() else ""
        volume=category_all_goods["data"][i]['volume'] if 'volume' in category_all_goods["data"][i].keys() else ""
        zk_final_price=category_all_goods["data"][i]['zk_final_price'] if 'zk_final_price' in category_all_goods["data"][i].keys() else ""
        
        list1.append(pict_url)
        list1.append(click_url)
        list1.append(commission_rate)
        list1.append(coupon_amount)
        list1.append(item_description)
        list1.append(nick)
        list1.append(presale_discount_fee_text)
        list1.append(small_images)
        list1.append(title)
        list1.append(volume)
        list1.append(zk_final_price)

    list2=[]
    for i in range(0,len(list1),11):
        list2.append(list1[i:i+11])
    return HttpResponse(json.dumps({'total':list2}))
    
    
    
    

    
def taobao_picture_upload(request):
    pass  
    
    
    
def video_upload():
    pass
    
    
    
def Nine_nine(request):
    username=request.GET.get("username")
    if username==None:
        username=request.session.get("username")
    tbaok_anzones=tbaok_anzone.objects.filter(Q(user_name=username) & Q(status=1))
    return render(request,"microblog/Nine_nine.html",{"username":username,"tbaok_anzones":tbaok_anzones})
from microblog.nice import srarch_9
def get_nice_all(request):
    exclusive=request.POST.get("exclusive")
    category=request.POST.get("category")
    price=request.POST.get("price")
    now_page=request.POST.get("now_page")
    keyword=request.POST.get("keyword")
    
    print("当前页",now_page)
    
    if price=="":
        price=10
      
    if category=="":
        category="淘客佣金降序"

    dt=srarch_9(keyword,now_page,exclusive.split(" ")[1],price,category)
    list1=[]  

    for i in range(len(dt)):
        pict_url="<img style='width:200px;height:200px' src="+dt[i]["pict_url"]+">"
        item_url="<a target='_blank' href="+dt[i]["item_url"]+">商品详情</a>"
        commission_rate=dt[i]["commission_rate"] 
        coupon_info=dt[i]["coupon_info"]
        print(coupon_info) 
        try:
            coupon_end_time=dt[i]["coupon_end_time"] 
        except:
            coupon_end_time=""
        shop_title=dt[i]["shop_title"] 
        title=dt[i]["title"] 
        zk_final_price=dt[i]["zk_final_price"] 
        volume=dt[i]["volume"] 

        list1.append(pict_url)
        list1.append(item_url)
        list1.append(commission_rate)
        list1.append(coupon_info)
        list1.append(coupon_end_time)
        list1.append(shop_title)
        list1.append(title)
        list1.append(zk_final_price)
        list1.append(volume)
        
    
    list2=[]
    for i in range(0,len(list1),9):
        list2.append(list1[i:i+9])  
    print(list2[0])
    return HttpResponse(json.dumps({'total':list2})) 

    
from Administrator.models import goods_video   
    
def goods_check_video(request):
    try:
        gid=request.POST.get("id")
        good_list=goods_video.objects.filter(video_goods_id=gid)
        
        list1=[]
        for g in good_list:
            list1.append(g.video_path)
        return HttpResponse(json.dumps({'total':list1})) 
    except:
        return HttpResponse(json.dumps({'total':"播放失败，请联系管理员"})) 
    
    
    return HttpResponse(json.dumps({'total':"视频"})) 
def goods_check_description(request):
    try:
        gid=request.POST.get("id")
        lans=lan_various.objects.filter(id=gid)
        for l in lans:
            return HttpResponse(json.dumps({'total':l.product_description})) 
    except:
        return HttpResponse(json.dumps({'total':"查询失败，请联系管理员"})) 
        

import requests
import time
def time_stamp1(timeStamp):

    timeArray = time.localtime(int(timeStamp))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return  otherStyleTime
def run1(list3):
    list2 = ["pict_url", "item_url", "commission_rate", "coupon_info", "coupon_start_time","coupon_end_time","shop_title","title","zk_final_price","volume"];
    dict={};
    i=0;
    length=len(list2);    
    while i<length:
        dit={list2[i]:list3[i]};
        dict.update(dit);
        i+=1;
    return dict;
def goods_link_info(new_page1):
    api='http://api.vephp.com/products?vekey=V00002707Y53998964&page=%s&pagesize=10'%new_page1
    resp=requests.get(api)
    jsn_dt=resp.json()['data']
    list1=[]
    for i in jsn_dt:
        pict_url="<img style='width:200px;height:200px' src='"+i["pict_url"]+"'>"#商品主图
        item_url="<a target='_blank' href='"+"https://detail.tmall.com/item.htm?id=%s"%i["item_id"]+"'>商品详情</a>"#商品链接
        commission_rate=i["commission_rate"] #佣金比率
        coupon_info="卷前价格:<span style='color:red'>"+i["zk_final_price"]+"</span><br>优惠卷总数:"+i["coupon_total_count"]+"<br>剩余优惠卷:"+i["coupon_remain_count"]#优惠券信息
        #优惠卷结束时间
        coupon_start_time =time_stamp1(i["coupon_start_time"])#开始时间
        coupon_end_time=time_stamp1(i["coupon_end_time"])#结束时间
        shop_title=i["shop_title"]#商品名称
        title=i["title"]#商品名称
        zk_final_price=float(i["zk_final_price"])-float(i["coupon_amount"])#最终售价
        volume=i["volume"]#销量
        list1.append(pict_url)
        list1.append(item_url)
        list1.append(commission_rate)
        list1.append(coupon_info)
        list1.append(coupon_start_time)
        list1.append(coupon_end_time)
        list1.append(shop_title)
        list1.append(title)
        list1.append(zk_final_price)
        list1.append(volume)
        
    list2=[]
    list3=[]
    for i in range(0,len(list1),10):
        list2.append(list1[i:i+10])
    for j in list2:
        list3.append(run1(j))
    return list2
def discounts(request):
    
    new_page1=request.POST.get("new_page1")
    print(new_page1)
    return HttpResponse(json.dumps({'total': goods_link_info(new_page1)}))
    
    
    
                 

    
    
    
    
    
    
    
    
    