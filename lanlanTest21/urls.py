"""lanlanTest21 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urpicture_uploadls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from app01 import views as app01_views
from artist import views as artist_views
from compile import views as compile_views
from django.conf import settings
from django.conf.urls.static import static
from django.views import static 
from audit import views as audit_views
from Administrator import views as Administrator_views
from microblog import views as microblog_views

urlpatterns = [
    url('admin/', admin.site.urls),
#     通用部分  登陆初始页
    url(r"^$",app01_views.app01_index,name="app01_index"),
#     登陆验证
    url(r"login_username",app01_views.login_username,name="login_username"),
#     任务领取第一步    --------  选择产品
    url(r"Get_task",app01_views.Get_task,name="Get_task"),
#     演员排行
    url(r"Artist_ranking",app01_views.Artist_ranking,name="Artist_ranking"),
#     样例视频
    url(r"sample_video",app01_views.sample_video,name="sample_video"),
#     上传剧本页面
    url(r"Upload_script",app01_views.Upload_script,name="Upload_script"),
#     剧本排行
    url(r"script_ranking",app01_views.script_ranking,name="script_ranking"),
#     最佳剧本
    url(r"Outstanding_drama",app01_views.Outstanding_drama,name="Outstanding_drama"),
#     艺人初始页
    url(r"artist_show",artist_views.artist_show,name='artist_show'),
    url(r"get_audit",artist_views.get_audit,name="get_audit"),
#     领取任务第二步-------选择剧本
    url(r"Allods_Gold",artist_views.Allods_Gold,name="Allods_Gold"),
#     上传视频
    url(r"upload_video",artist_views.upload_video),
#     删除任务
    url(r"del_task",artist_views.del_task,name="del_task"),
#     搜索剧本
    url(r"^search_article",artist_views.search_article,name="search_article"),
#    领取任务第二步-------选择剧本
    url(r"^get_play",artist_views.get_play,name="get_play"),
#     ajax 上传文件方法  没用
    url(r"upvideo",artist_views.upvideo,name="upvideo"),
#     编辑初始页
    url(r"compile_show",compile_views.compile_show,name="compile_show"),
#     上传剧本
    url(r"^upload_article",compile_views.upload_article,name="upload_article"),
#     获取剧本详细
    url(r"^check_content",compile_views.check_content,name="check_content"),
#     删除剧本
    url(r"^del_article",compile_views.del_article,name="del_article"),
#     没用
    url("refresh_article/$",compile_views.refresh_article,name="refresh_article"),
#     修改剧本页面
    url("update_article/$",compile_views.update_article,name="update_article"),
#     修改剧本
    url("update_db_article/$",compile_views.update_db_article,name="update_db_article"),
#     没用
    url("test1",app01_views.test1),  
    
#     审核
#     审核展示
    url(r"audit_show",audit_views.audit_show,name="audit_show"),
#     查看视频
    url(r"cheakvideo",audit_views.cheakvideo,name="cheakvideo"),
#     审核通过操作
    url(r"pass_the_audit",audit_views.pass_the_audit,name="pass_the_audit"),
#     审核不通过操作
    url(r"Not_approved",audit_views.Not_approved,name="Not_approved"),
#     查看审核记录
    url(r"cheakaduit",audit_views.cheakaduit,name="cheakaduit"),
#     审核撤回
    url(r"withdraw",audit_views.withdraw,name="withdraw"),
    
    
#     管理员

#     管理员展示
    url(r"Administrator_show",Administrator_views.Administrator_show,name="Administrator_show"),
#     管理员获取成员角色
    url(r"Acquire_role",Administrator_views.Acquire_role,name="Acquire_role"),
#     编剧管理
    url(r"scriptwriter_manage",Administrator_views.scriptwriter_manage,name="scriptwriter_manage"),
#     演员管理
    url(r"actor_manage",Administrator_views.actor_manage,name="actor_manage"),
#     审核管理
    url(r"manage_audit",Administrator_views.audit_manage,name="audit_manage"),
#     添加成员
    url(r"add_user",Administrator_views.add_user,name="add_user"),
#     删除成员
    url(r"del_user",Administrator_views.del_user,name="del_user"),
    
    
    url(r"get_compile",compile_views.get_compile,name="get_compile"),
    url(r"actual",compile_views.actual,name="actual"),
    url(r"sadhskajsh",artist_views.sadhskajsh,name="sadhskajsh"),
    url(r"get_title",artist_views.get_title,name="get_title"),
    url(r"get_product",artist_views.get_product,name="get_product"),
    url(r"look_all",artist_views.look_all,name="look_all"),
#     查看所有剧本
    url(r"all_compile",compile_views.look_all_compile,name="look_all_compile"),
    url(r"mistake",app01_views.mistake,name="mistake"),
#     管理员分发url
    url(r"^Administrator/",include(("Administrator.urls","Administrator"),namespace="Administrator")),   
#     选货操作 
    url(r'^bootstrapTable/',app01_views.bootstrapTable,name="bootstrapTable"),
#     选货上传图片上传链接的操作
    url(r'^getdata1/',app01_views.getdata1),
   
    url(r"^picture_upload",app01_views.picture_upload,name="picture_upload"),
    
    
#     淘宝联盟


    url(r"^microblog_user_show",microblog_views.microblog_user_show,name="microblog_user_show"),
    
    
    
    url(r"^choose_product",microblog_views.choose_product,name="choose_product"),
    

    url(r"^add_platform_user",microblog_views.add_platform_user,name="add_platform_user"),
    url(r"^get_already_have",microblog_views.get_already_have,name="get_already_have"),
    
    url(r"^get_exclusive_links",microblog_views.get_exclusive_links,name="get_exclusive_links"),
    url(r"^get_already_link",microblog_views.get_already_link,name="get_already_link"),
    
    url(r"^get_promotion",microblog_views.get_promotion,name="get_promotion"),
    
#     跳转页
    url(r"look_manifest",Administrator_views.look_manifest,name="look_manifest"),
    
#     详细数据请求
    url(r'^get_lnnkj/',Administrator_views.get_lnnkj,name="get_lnnkj"),
    
    url(r"^microblog/",include(("microblog.urls","microblog"),namespace="microblog")),   
    
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
    
    
    url(r'^Goods_upload/',microblog_views.Goods_upload,name="Goods_upload"),
    
    url(r'^get_good_particulars/',Administrator_views.get_good_particulars,name="get_good_particulars"),

#本人详细数据
    url(r'^Order_details/',microblog_views.Order_details,name="Order_details"),
#     以推广产品
    url(r'^Generalize_product/',microblog_views.Generalize_product,name="Generalize_product"),
    
    
#     大淘客
    url(r"^Transition_zone",microblog_views.Transition_zone,name="Transition_zone"),
    url(r"^guest_links",microblog_views.guest_links,name="guest_links"),
    
#     双十一
#     url(r"^Double_Eleven",microblog_views.Double_Eleven,name="Double_Eleven"),
    
    
    
#     url(r"^get_double_eleven",microblog_views.get_double_eleven,name="get_double_eleven"),
    
    
    url(r"^Eleven_Double",microblog_views.Eleven_Double,name="Eleven_Double"),
    url(r"^get_double_eleven1",microblog_views.get_double_eleven1,name="get_double_eleven1"),
    
    
#     大淘客图片上传
    url(r"^taobao_picture_upload",microblog_views.taobao_picture_upload,name="taobao_picture_upload"),
    url(r"^video_upload",microblog_views.video_upload,name="video_upload"),
    
    
#     9块9
    url(r"^Nine_nine",microblog_views.Nine_nine,name="Nine_nine"),
    url(r"^get_nice_all",microblog_views.get_nice_all,name="get_nice_all"),
    
    
    url(r"^goods_picture_upload",Administrator_views.goods_picture_upload,name="goods_picture_upload"),
    url(r"^describe_upload",Administrator_views.describe_upload,name="describe_upload"),
    url(r"task_upload",Administrator_views.task_upload),
    
   
    
    url(r"^goods_check_video",microblog_views.goods_check_video,name="goods_check_video"),
    url(r"^goods_check_description",microblog_views.goods_check_description,name="goods_check_description"),
    
    url(r"^discounts",microblog_views.discounts,name="discounts"),
    
    
    url(r"abc",Administrator_views.abc),
    
    url(r"^get_secondary",Administrator_views.get_secondary,name="get_secondary"),
    
]
 

import app01

handler404 = app01.views.page_not_found

handler500 = app01.views.page_not_found


handler403 = app01.views.page_not_found









