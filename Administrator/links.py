

# import requests
# 
# def goods_link_info(url):
#     api='http://api.vephp.com/hcapi?vekey=V00002707Y53998964' \
#         '&para={}&pid=mm_628620083_962250410_109573700113&detail=1'.format(url)
# 
#     resp=requests.get(api)
#     jsn_dt=resp.json()['data']
#     print(jsn_dt)
#     
#     
# goods_link_info("https://item.taobao.com/item.htm?id=598686977477")


import requests
import time
def time_stamp(timeStamp):

    timeArray = time.localtime(int(timeStamp))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(otherStyleTime) 
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

def goods_link_info():
    api='http://api.vephp.com/products?vekey=V00002707Y53998964&page=1&pagesize=100'
    resp=requests.get(api)
    jsn_dt=resp.json()['data']
    list1=[]
    print(jsn_dt)
    for i in jsn_dt:
        pict_url="<img style='width:200px;height:200px' src='"+i["pict_url"]+"'>"#商品主图
        item_url="<a target='_blank' href='"+"https://detail.tmall.com/item.htm?id=%s"%i["item_id"]+"'>商品详情</a>"#商品链接
        commission_rate=i["commission_rate"] #佣金比率
        coupon_info="卷后价格"+i["zk_final_price"]+"优惠卷总数:"+i["coupon_total_count"]+"   剩余优惠卷:"+i["coupon_remain_count"]#优惠券信息  
        #优惠卷结束时间
        coupon_start_time =i["coupon_start_time"]#开始时间
        coupon_end_time=i["coupon_end_time"]#结束时间
        shop_title=i["shop_title"]#商品名称
        title=i["title"]#商品名称
        zk_final_price=i["coupon_amount"]#最终售价
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
    print(list2[0])
    return list3
    
    
goods_link_info()




# 
#         dict1["pict_url"]="<img style='width:200px;height:200px' src='"+i["pict_url"]+"'>"
#         dict1["item_url"]="<a target='_blank' href='"+"https://detail.tmall.com/item.htm?id=%s"%i["item_id"]+"'>商品详情</a>"
#         dict1["commission_rate"]=i["commission_rate"]
#         dict1["coupon_info"]="优惠卷总数:"+i["coupon_total_count"]+"   剩余优惠卷:"+i["coupon_remain_count"]
#         dict1["coupon_start_time"]=time_stamp(i["coupon_start_time"])
#         dict1["coupon_end_time"]=time_stamp(i["coupon_end_time"])
#         dict1["shop_title"]=i["shop_title"]
#         dict1["title"]=i["title"]
#         dict1["zk_final_price"]=i["zk_final_price"]
#         dict1["volume"]=i["volume"]
#         print(dict1)
#         list1.append(dict1)
#     print(list1)