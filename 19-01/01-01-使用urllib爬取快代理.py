import socket
from urllib import request
from urllib import parse
from multiprocessing import Pool
from logging import getLogger
from lxml import etree
from pymongo import MongoClient
from urllib.request import ProxyHandler, build_opener


class SpiderKDL(object):
    
    def __init__(self,url, timeout=None, headers=None,):
        """
        函数初始化
        """
        self.url = url
        self.timeout = timeout
        self.headers = headers
        self.logger = getLogger(__name__)
        self.client = MongoClient('localhost',27018)
        
    def run(self):
        """
        使用进程
        """
        pools = Pool(4)
        for i in range(4):
            pools.apply_async(self.insert_data())
        pools.close()
        pools.join()

    def request(self):
        """
        请求数据
        """
        req = request.Request(url=self.url, headers=headers,)
        try:
            reqs = request.urlopen(req, timeout=self.timeout)
            response = reqs.read().decode('utf-8')
            html = etree.HTML(response)
            trs = html.xpath('//*[@id="list"]/table/tbody/tr')
            for tr in trs:
                ip = tr.xpath('./td[@data-title="IP"]/text()')[0]
                port = tr.xpath('./td[@data-title="PORT"]/text()')[0]
                if self.coll.find_one({'ip':ip}) == None:
                    if self.vs_http(host=ip, port=port):
                        jsons = {
                            'ip': ip,
                            'port':port,
                            'niming': tr.xpath('./td[@data-title="匿名度"]/text()')[0],
                            'type': tr.xpath('./td[@data-title="类型"]/text()')[0],
                            'address': tr.xpath('./td[@data-title="位置"]/text()')[0],
                            'run': tr.xpath('./td[@data-title="响应速度"]/text()')[0],
                            'last_time': tr.xpath('./td[@data-title="最后验证时间"]/text()')[0],
                        }
                        yield jsons
                else:
                    print("数据存在....")
                    yield None

        except request.URLError as e:
            if e.reason == socket.timeout:
                self.logger.debug("请求超时")
            else:
                self.logger.debug("请求出错")
                

    def connect(self,host=None,port=None, db=None, collections=None):
        """
        连接数据库
        存储数据
        """
        db = self.client[db]
        collection = db[collections]
        return collection
        

    def insert_data(self):
        """
        存储数据
        """
        self.coll = self.connect(host='localhost', port=27018, db='kdl', collections='coll_data')
        for json in self.request():
            if self.coll.find_one(json):
                pass
            else:
                if json:
                    insert_id = self.coll.insert_one(json).inserted_id
                    print("数据存储成功 --- >> %s" % insert_id)
                else:
                    print("地址连接超时")

    def qu_chong(self, data):
        """
        
        
        """
        return set(data)

    
    def __del__(self):
        self.client.close()


    def vs_http(self, host, port):
        """
        验证代理ip是否可用
        """
        proxy = ProxyHandler(self.setProxy(host, port))
        opner = build_opener(proxy)
        headers = {
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                    'Host':'www.baidu.com',
                }
        req = request.Request('https://www.baidu.com/', headers=headers)
        try:
            response = opner.open(req, timeout=5)
            if response:
                print("验证成功...开始存储数据")
                return True
        except request.URLError as e:
            print(e.reason)
            return False
    

    def setProxy(self, host, port):
        print("使用代理:"+host+':'+port)
        return {'http':host+ ':' + port}
        

if __name__ == "__main__":

    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Host':'www.kuaidaili.com',
    }
    
    for i in range(1,2000):
        url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i)
        spider = SpiderKDL(url=url, timeout=5000, headers=headers)
        # spider.request()
        spider.run()
