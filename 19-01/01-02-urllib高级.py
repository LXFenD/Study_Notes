
from  urllib import request
from http import cookiejar


"""
 获取百度的cookie 并且遍历cookie
 设置请求头
"""
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Host': 'www.baidu.com',
}
cookie =  cookiejar.CookieJar()
def requesrBaidu(cookie, headers,url='https://www.baidu.com', timeout=5, is_read=False):

    handler = request.HTTPCookieProcessor(cookie)
    opner = request.build_opener(handler)
    req = request.Request(url, headers=headers)
    response = opner.open(req, timeout=timeout)
    for item in cookie:
        print(item.name +'='+ item.value)
        
    if is_read:
        print(response.read().decode('utf-8'))

"""
保存cookie到文件
"""
filanname="/home/hujian/文档/Study_Notes/19-01/01-02-cookie-01.txt"
cookie = cookiejar.MozillaCookieJar(filanname)
requesrBaidu(cookie, headers)
cookie.save(ignore_discard=True, ignore_expires=True)


"""
将cookie保存为lwp格式
"""

filanname="/home/hujian/文档/Study_Notes/19-01/01-02-cookie-02.txt"
cookie = cookiejar.LWPCookieJar(filanname)
requesrBaidu(cookie, headers)
cookie.save(ignore_discard=True, ignore_expires=True)


"""
读取存储的cookie值
"""

cookie = cookiejar.LWPCookieJar()
cookie.load(filanname, ignore_discard=True, ignore_expires=True)
requesrBaidu(cookie, headers, is_read=True)

