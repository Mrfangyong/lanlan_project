import requests
from lxml import html
import pandas
etree=html.etree
def get_data(i):
    resp=requests.get('http://cms.vogueda.com/freeplatformCms/purchase/listEspeciallyInventoryIId/{}.htm'.format(i))
    htmm=etree.HTML(resp.text)
    tr_list=htmm.xpath('//table[@class="data-grid"]/tr')
    l1,l2,l3,l4,l5,l6,l7,l8,l9=[],[],[],[],[],[],[],[],[]
    for tr in tr_list:
        td_list=tr.xpath('./td')
        goods_id=td_list[1].xpath('./b/text()')[0].strip();#l1.append(goods_id)    #款式编码
        image_url=td_list[1].xpath('./a/img/@src')[0].strip() if len(td_list[1].xpath('./a/img/@src'))>0 else '无数据';   #图片链接
        kucun = td_list[2].xpath('./span/text()')[0].strip();#l2.append(kucun)    #库存数
        ban_status= td_list[2].xpath('./span/text()')[1].strip();#l3.append(ban_status)    #版状态
        ban_date=td_list[2].xpath('./span/text()')[2].strip();#l4.append(ban_date)    #送版日期  下表3的是还版日期
        jijie = td_list[2].xpath('./span/text()')[4].strip();#l5.append(jijie)     # 季节标签
        son_tr_list=td_list[3].xpath('./table/tbody/tr[@style]')
        for sontr in  son_tr_list:
            shangpinbianma=sontr.xpath('./td[2]/text()')[0].strip();l6.append(shangpinbianma)
            yanseguige=sontr.xpath('./td[3]/text()')[0].strip();l7.append(yanseguige)
            kucunshuliang=sontr.xpath('./td[4]/text()')[0].strip();l8.append(kucunshuliang)
            # l1+=[goods_id]*len(shangpinbianma)
            # l2+= [kucun] * len(shangpinbianma)
            # l3 += [ban_status] * len(shangpinbianma)
            # l4 += [ban_date] * len(shangpinbianma)
            # l5 += [jijie] * len(shangpinbianma)
            l1.append(goods_id)
            l2.append(kucun)
            l3.append(ban_status)
            l4.append(ban_date)
            l5.append(jijie)
            l9.append(image_url)
    colu=['goods_id',"kucun","ban_status","ban_date","jijie","shangpinbianma","yanseguige","kucunshuliang",'image_url']
    return pandas.DataFrame([l1,l2,l3,l4,l5,l6,l7,l8,l9],index=colu).T
    # pandas.DataFrame([l1,l2,l3,l4,l5,l6,l7,l8],index=colu).T.to_excel("聚仓商品.xlsx")

if __name__ == '__main__':
    all_dt=pandas.DataFrame()
    for i in range(1,22):
        print(i)
        dt=get_data(i)
        all_dt=all_dt.append(dt)
    all_dt.to_excel("所有聚仓数据.xlsx")