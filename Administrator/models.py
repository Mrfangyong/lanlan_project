from django.db import models


# Create your models here.



#     Design_code Image_path inventory format_state Delivery_date change_date Season_label is_putaway
    
#     款式编码    
#     图片路径
#     库存量
#     版式状态
#     松板时间
#     换版时间
#     季节标签

# commodity_code color_specifications Stock_Quantity Image_state img_path variouss
#     序号
# 商品编码putaway='款式已使用，图片已上传'
# 颜色规格
# 库存数量
# Design_code  Image_path inventory unit_price Season_label putaway item_link zk_final_price title commission_rate coupon_info volume status
class lan_various(models.Model): 
    Design_code=models.CharField(max_length=225)
    Image_path=models.CharField(max_length=225)
    inventory=models.IntegerField()
    unit_price=models.CharField(max_length=225)
    Season_label=models.CharField(max_length=225)
    putaway=models.CharField(max_length=225)
    item_link=models.CharField(max_length=500)
    
    zk_final_price=models.CharField(max_length=225)
    title=models.CharField(max_length=225)
    commission_rate=models.CharField(max_length=225)
    coupon_info=models.CharField(max_length=225)
    volume=models.CharField(max_length=225)
    create_time=models.DateTimeField(auto_now_add=True)
    
    product_description=models.TextField()
    
    status=models.CharField(max_length=225)

class lan_various_category(models.Model):
    commodity_code=models.CharField(max_length=225)
    color_specifications=models.CharField(max_length=225)
    Stock_Quantity=models.IntegerField()
    
    variouss=models.ForeignKey(lan_various,on_delete=models.CASCADE)
    
class lan_various_img(models.Model):
    img_name=models.CharField(max_length=225)
    img_path=models.CharField(max_length=225)
    various_img=models.ForeignKey(lan_various,on_delete=models.CASCADE)    



class tbaok_anzone(models.Model):
    user_name=models.CharField(max_length=225)
    adzone_name=models.CharField(max_length=225)
    platform=models.CharField(max_length=225)
    account_name=models.CharField(max_length=225)
    adzone_id=models.CharField(max_length=225)
    status=models.CharField(max_length=225,default="0")

#    category_id coupon_click_url coupon_end_time coupon_info coupon_remain_count coupon_start_time coupon_total_count coupon_type
#    commission_rate num_iid tbk_pwd coupon_short_url request_time user_name my_tb_link adzone_id
class links_convert(models.Model):
    category_id=models.IntegerField()
    coupon_click_url=models.CharField(max_length=225)
    coupon_end_time=models.CharField(max_length=225)
    coupon_info=models.CharField(max_length=225)
    coupon_remain_count=models.CharField(max_length=225)
    coupon_start_time=models.CharField(max_length=225)
    coupon_total_count=models.CharField(max_length=225)
    coupon_type=models.CharField(max_length=225)
    commission_rate=models.CharField(max_length=225)
    num_iid=models.CharField(max_length=225)
    tbk_pwd=models.CharField(max_length=225)
    coupon_short_url=models.CharField(max_length=225)
    request_time=models.CharField(max_length=225)
    user_name=models.CharField(max_length=225)
    my_tb_link=models.CharField(max_length=500)
    adzone_id=models.CharField(max_length=225)
    




class order(models.Model):
    
    tb_paid_time=models.CharField(max_length=225)  
    tk_paid_time=models.CharField(max_length=225)
    pay_price  =models.CharField(max_length=225)
    pub_share_fee  =models.CharField(max_length=225)
    trade_id  =models.CharField(max_length=225)
    tk_order_role =models.CharField(max_length=225)
    tk_earning_time=models.CharField(max_length=225)
    adzone_id =models.CharField(max_length=225)
    pub_share_rate =models.CharField(max_length=225)
    refund_tag  =models.CharField(max_length=225)
    subsidy_rate  =models.CharField(max_length=225)
    tk_total_rate  =models.CharField(max_length=225)
    item_category_name  =models.CharField(max_length=225)
    seller_nick =models.CharField(max_length=225)
    pub_id  =models.CharField(max_length=225)
    alimama_rate =models.CharField(max_length=225)
    subsidy_type  =models.CharField(max_length=225)
    item_img  =models.CharField(max_length=225)
    pub_share_pre_fee  =models.CharField(max_length=225)
    alipay_total_price =models.CharField(max_length=225)
    item_title  =models.CharField(max_length=225)
    site_name  =models.CharField(max_length=225)
    item_num =models.IntegerField()
    subsidy_fee=models.CharField(max_length=225)
    alimama_share_fee  =models.CharField(max_length=225)
    trade_parent_id =models.CharField(max_length=225)
    order_type =models.CharField(max_length=225)
    tk_create_time  =models.CharField(max_length=225)
    flow_source  =models.CharField(max_length=225)
    terminal_type =models.CharField(max_length=225)
    click_time =models.CharField(max_length=225)
    tk_status =models.CharField(max_length=225)
    item_price  =models.CharField(max_length=225)
    item_id =models.CharField(max_length=225)
    adzone_name =models.CharField(max_length=225)
    total_commission_rate=models.CharField(max_length=225)
    item_link  =models.CharField(max_length=225)
    site_id  =models.CharField(max_length=225)
    seller_shop_title =models.CharField(max_length=225)
    income_rate  =models.CharField(max_length=225)
    total_commission_fee  =models.CharField(max_length=225)
    tk_commission_pre_fee_for_media_platform =models.CharField(max_length=225)
    tk_commission_fee_for_media_platform =models.CharField(max_length=225)
    tk_commission_rate_for_media_platform  =models.CharField(max_length=225)

class goods_video(models.Model):
    video_title=models.CharField(max_length=255)
    video_path=models.CharField(max_length=255)
    video_goods=models.ForeignKey(lan_various,on_delete=models.CASCADE)































