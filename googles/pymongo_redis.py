# -*- coding: utf8 -*-
import pymongo
import redis

client = pymongo.MongoClient('localhost:27009')
db = client['RENMIN']#变更学校
col=db['化学系_papers']#变更学院


def GetPaperAuthors():
    s=set()
    for i in col.find():
        for a in i['author']:
            s.add(a['name'])
    return s




def ToRedis():#变更host
    db=redis.StrictRedis(host='localhost',#host='localhost'host='123.206.177.39'
                         port='6379',
                         db =3,
                         decode_responses=True,
                         password='try_123as_pass')#password='try_123as_pass'
    s=GetPaperAuthors()
    for i in s:
        db.set(i,i)
    print('OK')
ToRedis()
