# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import re
import time
import redis
import random
import base64
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from googles.GetUserAgents_from_web import ua_list_now


"""----------------------------------------------------------"""
#abuyun代理服务器
proxyServer = "http://proxy.abuyun.com:9020"
# 代理隧道验证信息
proxyUser = "H264P9E9M949159D"
proxyPass = "1C6AED9CB122390C"
# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
# for Python2
#proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)
"""----------------------------------------------------------"""
############################################################################################################################

"""=========================================================="""
#vps代理服务器
db=redis.StrictRedis(host='localhost',port='6379',db = 0,decode_responses=True,password='try_123as_pass')
"""=========================================================="""


baiduheaders={
'X-Requested-With':'XMLHttpRequest',
'is_xhr':'1',
'Host':'www.baidu.com',
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate, sdch, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
    }

cacheheaders = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdchAccept-Encoding:gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Upgrade-Insecure-Requests':'1',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    
}

class AbuyunProxiesMiddleware(HttpProxyMiddleware):
    proxies = {}
    def __init__(self, auth_encoding='latin-1'):
        self.auth_encoding = auth_encoding
        
        self.proxies[proxyServer] = proxyUser + proxyPass

    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth


    def process_response(self,request, response, spider):
        
        if response.status in [429,999]:
            time.sleep(1)
            return request
        else:
            return response
        
class VPSProxiesMiddleware(HttpProxyMiddleware):
    def process_request(self, request, spider):    
        if db.keys():
            proxies = [db.get(key) for key in db.keys()]
            request.meta["proxy"] = 'http://'+proxies[0]
            #print(request.headers)
        else:
            time.sleep(1)
    def process_response(self,request, response, spider):
        
        if response.status in [429,500,501,502,503,504,999]:
            time.sleep(5)
            return request
        else:
            return response
        

class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self,user_agent=''):
        self.user_agent =user_agent
 
    def process_request(self, request, spider):
        #这句话用于随机选择user-agent
        ua = random.choice(ua_list_now)


        if re.search('linkedin.com',request.url):
            request.replace(headers=cacheheaders)
            request.headers.setdefault(b'Host','cn.linkedin.com')
        if self.user_agent:
            request.headers.setdefault(b'User-Agent', ua)
