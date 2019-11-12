'''
Created on 2019年8月29日

@author: 19160
'''

from django.conf.urls import url
from .views import get_particular,get_all_img,user_cargo,search,del_picture,goods_link_info,del_goods
urlpatterns=[
    url(r"^get_particular/",get_particular,name="get_particular"),
    url(r"^get_all_img/",get_all_img,name="get_all_img"),
    url(r"^user_cargo/",user_cargo,name="user_cargo"),
    url(r"^search/",search,name="search"),
    url(r"^del_picture/",del_picture,name="del_picture"),
    url(r"^goods_link_info/",goods_link_info,name="goods_link_info"),
    
    url(r"^del_goods/",del_goods,name="del_goods"),
    
    
    ]
