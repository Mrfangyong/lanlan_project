'''
Created on 2019年8月6日

@author: 19160
'''
import requests



api2='http://api.vephp.com/hcapi?vekey=V00002707Y53998964&para=575731102837&pid=mm_462280062_664500316_109231150257'
resp2=requests.get(api2)

print(dir(resp2))
print(resp2.content)
print(resp2.text)


# 
# 
# {"result":1,"data":{"category_id":"1801","coupon_click_url":"https://uland.taobao.com/coupon/edetail?e=3Z8dvjtUcLIGQASttHIRqe5cu%2BLwclMH2z37nT2ymOV%2FE8arSGg6K%2BWe0Di6W63FvHxGyWL6xs6I4he9xbIKbEHSH1bGor0AIJ1GtccYOa7CKbsAbM2TPOT3b4zuHjpz1ug731VBEQm1M7QmaYJz9PFaBe2GOkPYHvfjMSYvfkGji5Mwp8diMAxbyS5oaMOQepVc1Ap6UyHul8YkAYJFPraz4V0OHQGD&traceId=0b82da9115680951665493594e&union_lens=lensId:0b0fc0d4_0bf5_16d19c1606e_4777&xId=dJvyRvBO2P4yZFAUzhna4S2vx0aIchIozGkUA0HUGiNVlKJoLcETl8FFaavTlRULZ3tajj65HTj6IDRA9RugRw","coupon_end_time":"2019-09-10","coupon_info":"满103元减25元","coupon_remain_count":"9900","coupon_start_time":"2019-09-09","coupon_total_count":"10000","coupon_type":"3","commission_rate":"0.90","num_iid":"575731102837","tbk_pwd":"￥bJaIYOmFeQ1￥","coupon_short_url":"https://s.click.taobao.com/en77J1w"}}





