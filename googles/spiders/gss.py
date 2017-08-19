# -*- coding: utf-8 -*-
from scrapy import Request,Spider
import re
from bs4 import BeautifulSoup as bs
from urllib.parse import *
from googles.items import GooglesItem
import pymongo
import redis
import random
from xpinyin import Pinyin
from googles.GetUserAgents_from_web import ua_list_now
from googles.settings import MONGO_HOST
from googles.settings import SCHOOL_LIST


client = pymongo.MongoClient(MONGO_HOST)
db2=client['schools']
col2=db2['dpts_985']


class GsSpider(Spider):    
    name = 'golink'
    allowed_domains = ['linkedin.com']
    
    def start_requests(self):
        ua=random.choice(ua_list_now)
        ra=random.random()
        headers={'User-Agent':ua,
                 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                 'Accept-Encoding':'gzip, deflate',
                 'Accept-Language':'zh-CN,zh;q=0.8',
                 'Cache-Control':'max-age=0',
                 'Connection':'keep-alive',
                 'Upgrade-Insecure-Requests':'1',
                 }
        for short in SCHOOL_LIST:
            db=client[short+'c']
            dpts=col2.find_one({'short':short})['dpts']
            for dpt in dpts:
                col=db[dpt+'_studentsLinku']
                NAME_LIST=[]
                
                for item in col.find():
                    del item['_id']
                    if item['name_code'] not in NAME_LIST:
                        NAME_LIST.append(item['name_code'])
                        yield Request(item['url'],
                                  meta={'item':item,
                                        'dont_redirect':True,
                                        'cookiejar':ra,
                                        },
                                  headers=headers,                          
                                  callback=self.parse_linkedin,
                                      dont_filter=True)
                    else:
                        continue
            
    def parse_linkedin(self,response):
        item= GooglesItem()
        del response.meta['item']['_id']
        for key in response.meta['item'].keys():
            item[key]=response.meta['item'][key]

        soup=bs(response.text,'lxml')

        if soup.find_all('li',class_='position'):#section[experience>ul[positions:
            item['experience']=[]
            for piece in soup.find_all('li',class_='position'):

                exp={}

                #公司名称以书写版和领英版都要有,logo部分是领英给出的，item-subtitle是自己写的
                if piece.find('h5',class_='logo'):
                    if piece.find('h5',class_='logo').a:
                        company_url_ly=piece.find('h5',class_='logo').a.attrs['href']
                        
                        company_name_ly=piece.find('h5',class_='logo').a.img.attrs['alt']
                        exp['company_url_ly']=company_url_ly
                        exp['company_name_ly']=company_name_ly
                if piece.find('h5',class_='item-subtitle'):
                    company_name=piece.find('h5',class_='item-subtitle').get_text()
                    exp['company_name']=company_name
                    if piece.find('h4',class_='item-title'):
                        position_title=piece.find('h4',class_='item-title').get_text()
                        exp['position_title']=position_title
                    if piece.find('h5',class_='item-subtitle').a:
                        if 'href' in piece.find('h5',class_='item-subtitle').a.attrs:
                            company_url_ha=piece.find('h5',class_='item-subtitle').a.attrs['href']
                            exp['company_url_ha']=company_url_ha
                if piece.find('span',class_='date-range'):#company
                    date_range=piece.find('span',class_='date-range').get_text(strip=True).split('(')[0].split('-')
                    exp['date_range']=date_range
                if piece.find('span',class_='location'):#company
                    location=piece.find('span',class_='location').get_text()
                    exp['location']=location

                item['experience'].append(exp)


                
        if soup.find_all('li',class_='school'):#section[education>ul[schools:
            item['education']=[]
            for piece in soup.find_all('li',class_='school'):
                
                edu={}
                
                if piece.find('h5',class_='logo'):
                    if piece.find('h5',class_='logo').a:
                        school_url_ly=piece.find('h5',class_='logo').a.attrs['href']
                        school_name_ly=piece.find('h5',class_='logo').a.img.attrs['alt']
                        edu['school_url_ly']=school_url_ly
                        edu['school_name_ly']=school_name_ly
                if piece.find('h4',class_='item-title'):
                    school_name=piece.find('h4',class_='item-title').get_text()
                    edu['school_name']=school_name
                    if piece.find('h4',class_='item-title').a: 
                        school_url=piece.find('h4',class_='item-title').a.attrs['href']
                        edu['school_url']=school_url
                if piece.find('h5',class_='item-subtitle'):
                    if piece.find('h5',class_='item-subtitle').find('span',class_='original translation'):                                       
                        degree_name=piece.find('h5',class_='item-subtitle').find('span',class_='original translation').get_text()
                        edu['degree_name']=degree_name
                if piece.find('span',class_='date-range'):
                    date_range=piece.find('span',class_='date-range').get_text()
                    edu['date_range']=date_range
                if piece.find('div',class_='description'):
                    if piece.find('div',class_='description').p:
                        description=[]
                        for pi in piece.find('div',class_='description').find_all('p'):
                            description.append(pi.get_text(strip=True))
                            edu['description']=description

                item['education'].append(edu)


        insights=soup.find('section',class_='insights')
        if insights:
            browse=insights.find('div',class_='browse-map')
            if browse and browse.find_all('li',class_='profile-card'):
                item['mapLink']=[]
                for li in browse.find_all('li',class_='profile-card'):
                    map_link={}
                    map_link['name']=li.h4.a.get_text()
                    map_link['link']=li.h4.a.attrs['href']
                    item['mapLink'].append(map_link)
                

            
        if soup.find('section',id='publications'):
            pass

        if soup.find('section',id='projects'):
            pass

        if soup.find('section',id='awards'):
            pass

        if soup.find('section',id='skills'):
            pass

        if soup.find('section',id='languages'):
            pass

        if soup.find('section',id='scores'):
            pass

        if soup.find('section',id='certifications'):
            pass



        yield item
