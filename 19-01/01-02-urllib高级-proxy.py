from urllib import request
from urllib import parse
from pymongo import MongoClient
from random import choice

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Host': 'www.baidu.com',
}


def connect(host, port, db, coll):
    """
        连接数据库
    """
    client = MongoClient(host, port)

    try:
        db = client[db]
        collection = db[coll]
        
        return collection
    except Exception:
        return None
    
def requesrBaidu(handler, headers,url='https://www.baidu.com', timeout=5, is_read=False):

    opner = request.build_opener(handler)
    req = request.Request(url, headers=headers)
    response = opner.open(req, timeout=timeout)
        
    if is_read:
        print(response.read().decode('utf-8'))


coll = connect('localhost', 27018, 'kdl', 'coll_data')
find = choice(list(coll.find()))
proxy_heandler = request.HTTPHandler(
    {
        'http':'http:%s:%s' % (find['ip'], find['port'])
    }
)
requesrBaidu(proxy_heandler,headers, is_read=True )
