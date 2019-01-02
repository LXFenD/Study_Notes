from selenium import webdriver
import requests 
import time
from lxml import etree
import pymongo
from pymongo import MongoClient
from datetime import datetime
from multiprocessing import  pool, Process

## options 设置不显示界面
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
browser = webdriver.Chrome()

browser.get('https://www.jianshu.com/trending/weekly?utm_medium=index-banner-s&utm_source=desktop')
for i in range(3):
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)


# for i in range(100):
#     try:
#         button = browser.execute_script('var a = document.getElementsByClassName("load-more"); a[0].click()')
#         browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#         time.sleep(2)
#     except:
#         pass

imgs = browser.find_elements_by_class_name('wrap-img')
have_img = browser.find_elements_by_class_name('have-img')
# browser.

headers = {
    'Referer': 'https://www.jianshu.com/',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
client = MongoClient('localhost',27018)
db = client.jianshu
coll = db.js_data
for img in range(len(imgs)):
    blog_url = imgs[img].get_attribute('href')
    img_src = imgs[img].find_element_by_tag_name('img')
    print(blog_url)
    blog_img = img_src.get_attribute('src')
    res = requests.get(blog_url, headers=headers)
    text = res.text
    # print(text)
    html = etree.HTML(text)
    content = html.xpath('')
    # content = etree.
    title = have_img[img].find_element_by_class_name('title')
    # print(content)
    print(content)
    cun = coll.find_one({'title':str(title.text)})

    if cun:
        print("存在了！！ 返回")
        continue
    # jsons = {
    #     'img':blog_img,
    #     'time': datetime.utcnow(),
    #     'title': title.text,
    #     'content':content[0],
    # }
    # print(jsons)
    # inserted_id = coll.insert_one(jsons).inserted_id
    # print(inserted_id)
    time.sleep(1)
