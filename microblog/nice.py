import requests
#排序方式：  total_sales_des（销量降序） tk_rate_des（淘客佣金比率降序）tk_rate_asc（淘客佣金比率升序）
#total_sales_des（销量降序） total_sales_asc（销量升序） tk_total_sales_des（累计推广量降序）
#tk_total_sales_asc（累计推广量升序）   tk_total_commi_des（总支出佣金降序）
#tk_total_commi_asc（总支出佣金升序）    price_des（价格降序）    price_asc（价格升序）
sort_dict={
'价格降序':'price_des',
'价格升序':'price_asc',
'销量降序':'total_sales_des',
'销量升序':'total_sales_asc',
'淘客佣金降序':'tk_rate_des',
'淘客佣金升序':'tk_rate_asc',
}
#前端要传的值：  搜索关键字（可以是商品链接  口令）
#pid   页数   最高价格   排序方式
def commission_rate_true(data,search_type):

    for dt in data:
        if search_type=='1':
            dt['commission_rate']=int(dt['commission_rate'])/100 if 'commission_rate' in dt else 0
        else:
            dt['commission_rate'] = dt['commission_rate'] if 'commission_rate' in dt else 0
        dt['pict_url']=dt['pict_url'] if 'pict_url' in dt else 0
        dt['item_url']=dt['item_url'] if 'item_url' in dt else 0
        dt['coupon_info']=dt['coupon_info'] if 'coupon_info' in dt else 0
        dt['shop_title']=dt['shop_title'] if 'shop_title' in dt else 0
        dt['title']=dt['title'] if 'title' in dt else 0
        dt['zk_final_price']=dt['zk_final_price'] if 'zk_final_price' in dt else 0
        dt['volume']=dt['volume'] if 'volume' in dt else 0
    return data
def srarch_9(words,page_nums,pid,end_price,sort):
    sort=sort_dict[sort]
    api='http://api.vephp.com/super?vekey=V00002707Y53998964&para={}' \
        '&start_price=1&end_price={}&sort={}&page={}&pid={}'.format(words,end_price,sort,page_nums,pid)
    resp=requests.get(api)
    jsn_dt=resp.json()
    #要显示的字段   #商品主图  pict_url，商品链接 item_url   佣金比例  commission_rate
    # 优惠卷信息 coupon_info  优惠卷结束时间 coupon_end_time   店铺名称 shop_title   商品名称  title
    #  最后售价 zk_final_price  近30天销量  volume
    if  jsn_dt['error']!='0':
        return '请求错误，请检查请求参数！'
    search_type=jsn_dt['search_type']#如果 search_type的值是1   那么所有的佣金比率字段要除100
    data = jsn_dt['result_list']
    data=commission_rate_true(data,search_type)
    return data
# 
# dt=srarch_9('裤子','1','mm_628620083_962250410_109573700113','10','淘客佣金降序')
# print(dt)

# pid 种草小星星 mm_628620083_963300373_109570800480
# 排序 淘客佣金降序
# 价格 50
# 当前页 1
# 关键词 裙子


