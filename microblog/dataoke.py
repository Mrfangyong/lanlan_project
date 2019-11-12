import requests
import hashlib
from urllib import parse
from dtk_open_platform import DtkOpenPlatform
send = DtkOpenPlatform()
appSecret= '1a0b2fe0c7b95a2e04cc3eff7389e88f'
appKey = '5db13a2b41fba'
version = 'v1.1.1' #当前版本号
def get_goods_detail(goodsId):
    try:#出发异常说明是代码错误
        url = 'https://openapi.dataoke.com/api/goods/get-goods-details'
        method = 'get'
        data = {'appKey': appKey,
                'version': version,
                # 'id':'22931441',#这个id是大淘客商品id   我们不支持这个操作
                'goodsId':goodsId,}
        response = send.open_platform_send(method=method,url=url,args=data,key=appSecret)
        if response['code']!=0: #不等于0说明是请求参数错误
            return 'error 0'
    except:
        return 'error 0'#获取商品详情出错
    return response

def dataoke_translate_link(pid,goodsId):
    try:
        url = 'https://openapi.dataoke.com/api/tb-service/get-privilege-link'
        method = 'get'
        data = {'appKey': appKey,
                'version': version,
                # 'id':'22931441',
                'goodsId': goodsId,
                'pid':pid,}
        
        response = send.open_platform_send(method=method, url=url, args=data, key=appSecret)
        print("返回的数据",response)
        if response['code']!=0: #不等于0说明是请求参数错误
            return 'error 1'
    except:
        return 'error 1'
    return response

def to_short(link):
    try:
        appKey2='956fbd867d59c75f2f41b6fc8b0332a2'#这个是我找的一个短链接生成api
        link=parse.quote(link)
        md5_link=hashlib.md5(link.encode()).hexdigest()
        sign=hashlib.md5((appKey2+md5_link).encode()).hexdigest()
        params={
            'appkey':appKey2,
            'long_url':link,
            'sign':sign,
        }
        resp=requests.get('http://www.mynb8.com/api/sina',params=params)
        jsn_dt=resp.json()
        if 'short_url' in jsn_dt.keys():
            return jsn_dt['short_url']
        else:#说明发生错误了
            return '生成短链接异常  可使用 http://tool.chinaz.com/tools/dwz.aspx 自主生成'
    except:
        return '生成短链接异常  可使用 http://tool.chinaz.com/tools/dwz.aspx 自主生成'

def to_short2(link):
    try:
        data = {'longUrl':link}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        resp = requests.post('http://tool.juanzhuzhu.com/url/short',headers=headers,data=data)
        jsn_dt=resp.json()
        if jsn_dt['status']==1:
            return jsn_dt['data']['url']
        else:#说明发生错误了
            return jsn_dt['info']
    except:
        return '生成短链接异常  可使用 http://tool.juanzhuzhu.com/ 自主生成'
def action(pid,goodsId):
    #要插入数据库的字段:
    detail_data=get_goods_detail(goodsId)
    if detail_data=='error 0':
        return '获取商品详情错误！'
    
    print("pid",pid)
    print("goodsId",goodsId)
    zhuanshu_link=dataoke_translate_link(pid,goodsId)
    if detail_data=='error 1':
        return '生成专属链接错误！'
    info="大淘客无此商品，显示淘宝联盟信息。(由于缓存原因，详情不一致的情况)" if detail_data['data']['id']==-1 else "显示大淘客内信息"
    desc=detail_data['data']['desc']
    
    try:
        tpwd=zhuanshu_link['data']['tpwd']#淘口令
        couponClickUrl=zhuanshu_link['data']['couponClickUrl']#专属链接
        couponEndTime=zhuanshu_link['data']['couponEndTime']#活动结束时间
        couponInfo=zhuanshu_link['data']['couponInfo']#优惠卷信息
        ss="明磊提示:"+info+"\n<br><br>"+"商品描述文案:"+desc+'\n<br><br>'+"淘口令:"+tpwd+'\n<br><br>'+"专属链接:"+couponClickUrl+'\n<br><br>'+"结束时间:"+couponEndTime+'\n<br><br>'+"优惠卷信息:"+couponInfo
        short_link=to_short(couponClickUrl)
        ss=ss+'\n<br><br>'+'短链接(微博可用):'+short_link
        return ss
    except:
        return "该item_id对应宝贝已下架或非淘客宝贝"
    
    



def insert_db():#插入数据库方法
    pass


# 1.大淘客商品  一键生成文案+专属链接
#:商品描述
#链接  淘口令
#商品短链接
#图片链接

print(to_short2("https://s.click.taobao.com/t?e=m%3D2%26s%3DsHPKNQzCSD1w4vFB6t2Z2ueEDrYVVa64Dne87AjQPk9yINtkUhsv0IYCP%2BW5uXNqYzVFs6a75XSkbdedeTvxJhpM7Yevb5%2FSV8eCgkbdtaiCs2LU%2BKQ7vzpI1PPHNUjdFBoMXOGuG5DkaqczTKGnOhFNXTdtWMyaxKQVLSayBBekOrGae4DS5oO2CiNcVz0Kq1W0d9Ob%2FLOG3sdWp9MJQ%2Bei79hRDyfknBf80C6qOF8%3D&scm=1007.15348.115058.0_26602&pvid=63165b0c-8b9f-4fcf-9492-ae4855b424da&app_pvid=59590_11.132.118.95_551_1572088246663&ptl=floorId:26602;originalFloorId:26602;pvid:63165b0c-8b9f-4fcf-9492-ae4855b424da;app_pvid:59590_11.132.118.95_551_1572088246663&union_lens=lensId%3An%401572088246%4063165b0c-8b9f-4fcf-9492-ae4855b424da_603629348336%401    "))














