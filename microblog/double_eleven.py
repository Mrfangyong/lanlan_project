import requests
from builtins import int

def get_shuangshiyi(type_name,pid,page_nums):#双十一预售商品接口
    type_dict = {
        "综合": 26481,
        "女装": 26595,
        "食品": 26599,
        "美妆个护": 26601,
        "家居家装": 26596,
        "数码家电": 26597,
        "母婴": 26598,
        "鞋包配饰": 26600,
        "男装": 26602,
        "内衣": 26603,
        "运动户外": 26604,
        "天猫国际": 26605
    }
    type_id=type_dict[type_name]
    api='http://api.vephp.com/presale?vekey=V00002707Y53998964&page_no={}&page_size=100&materialId={}&pid={}'.format(page_nums,type_id,pid)
    resp=requests.get(api)
    return resp.json()



category_all_goods=get_shuangshiyi("家居家装","mm_628620083_963300373_109570800480",3)


