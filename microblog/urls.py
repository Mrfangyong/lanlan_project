'''
Created on 2019年9月18日

@author: 19160
'''



from django.conf.urls import url
from .views import search
urlpatterns=[
    url(r"^search/",search,name="search"),

    
    
    ]


