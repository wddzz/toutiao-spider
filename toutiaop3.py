# -*- coding:utf-8 -*-
#get method
import requests  # python 3
import json
import re
import os
from hashlib import md5
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import RequestException

# 构造URL，向下滑动页面，获得所有的请求地址
def get_page_index(offset,keyword):
    #dict
    data = {
            'offset':offset,
            'format':'json',
            'keyword':keyword,
            'autoload':'true',
            'count':'20',
            'cur_tab':"1",
            'from':'search_tab'
            }
    #urlencode change the dict to the request parameters
    url = 'http://www.toutiao.com/search_content/?'+urlencode(data)
    print(url)
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print ('请求索引页出错！')
        return None

# parse JSON and get the url for every article
def parse_page_index(html):
    data=json.loads(html)
    #filter the object without data
    if data and 'data' in data.keys():
        item = str(data.get('data'))
        pattern = re.compile("image_list': \[\{'url': '(.*?)'", re.S)
        # print(pattern)
        result = pattern.findall(item)
        for url in result:
            yield ("http:" + url)
        # url_pattern = re.compile("image_detail': \[\{'url': '(.*?)'", re.S)
        # url_result = re.search(url_pattern,result)
        # urls_result = url_pattern.findall(url)
        # for url_result in urls_result:
        # print(url_result.group(1))
        # for url in url_result:
        #     yield url
#get the any one article
# def get_page_detail(url):
#     try:
#         response = requests.get(url)
#         if response.status_code==200:
#             return response.text
#         return None
#     except RequestException:
#         print ('请求详情页出错！')
#         return None

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print("下载图片出错")
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()


# def parse_page_detail(html,url):
#     # pattern = re.compile('BASE_DATA.galleryInfo = (.*?);',re.S)
#     pattern = re.compile('BASE_DATA.galleryInfo = (.*?)</script>', re.S)
#     # print(html)
#     result = re.search(pattern,html)
#     if not result:
#         print("aaa")
#         return None
#     data = result.group(1)

#     pattern_title = re.compile('title:(.*?),',re.S)
#     # print(result)
#     result2 = re.search(pattern_title,data)
#     #print(data)
#     title = result2.group(1)

#     # pattern_image = re.compile('gallery: JSON.parse\("(.*?)"\)')
#     pattern_image = data[data.index('JSON.parse("')+12:data.index('siblingList')-8]
#     result3 = re.search(pattern_image,data)
#     #print(result3.group(1))
#     jsonStr = re.sub(r'\\{1,2}', '',result3.group(1))
#     #print(jsonStr)


#     if result3:
#         data_image = json.loads(jsonStr)
#         if data_image and 'sub_images' in data_image.keys():
#             sub_images = data_image.get('sub_images')
#             images = [item.get('url') for item in sub_images]
#             for image in images:
#                 if image != "":
#                     download_image(image)
#             return {"title":title,
#                     "url":url,
#                     "images":images}

# #parse the any one article,request ask is OK,no need AJAX ask
# def parse_page_detail(html,url):
#     #print ('详情页解析结果：')
#     soup = BeautifulSoup(html,'lxml')
#     title = soup.select('title')[0].get_text()
#     #print (title)
#     #define regression and select the mode
#     #images_pattern = re.compile('sub_images([\s\S]*?)siblingList',re.S)
#     #result = re.search(images_pattern,html)
#     #print(result)
#     #data = json.loads(result)
#     #print(data['url'])

#     pattern = re.compile('sub_images([\s\S]*?)siblingList') #???
#     results = re.findall(pattern, html)
#     # if (len(results) > 0):
#     #     print(results[0])
#     download_image('http://p9.pstatp.com/large/4b020004bb17ae9a9235')

#     # result is a JSON need to parse the image url
#     if result:
#         #print result.group(1)
#         data=json.loads(result.group(1))
#         if data and 'sub_images' in data.keys():
#             sub_images=data.get('sub_images')
#             #list
#             images=[item.get('url') for item in sub_images]
#             return{
#                     'title':title,
# 					'url':url,
#                     'images':images
#                     }


def main():
    searchInfo = input("输入你需要的图片:")
    for i in range(0,141,20):
        html = get_page_index(i,searchInfo)
    #print ('AJAX请求返回结果：')
    #print (html)
        for url in parse_page_index(html):
            download_image(url)
        # print (url)
    # parse_page_index(html)
    # html=get_page_detail(html)
    # aaa = parse_page_index(html)
    # print(html)
    # if aaa:
        # result=parse_page_detail(html,url)
        # print (result)



if __name__=='__main__':
    main()
