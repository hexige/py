# -*-coding:utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
import http.cookiejar
import re
import time
import os.path


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
headers = {'User-Agent': user_agent}

question=27364360

def getImageUrl():
    url = "https://www.zhihu.com/node/QuestionAnswerListV2"
    method = 'next'
    size = 10
    allImageUrl = []

    #循环直至爬完整个问题的回答
    while(True):
        print ('===========offset: ', size)

        postdata = {       
            'method': 'next',
            'params': '{"url_token":' + str(question) + ',"pagesize": "10",' +\
                      '"offset":' + str(size) + "}",
         }
        size += 10
        page = requests.post(url, headers=headers, data=postdata)
        ret = eval(page.text)
        listMsg = ret['msg']

        if not listMsg:
            print ("图片URL获取完毕, 页数: ", (size-10)/10)
            return allImageUrl
        pattern = re.compile('data-actualsrc="(.*?)">', re.S)
        for pageUrl in listMsg:
            items = re.findall(pattern, pageUrl)
            for item in items:      #这里去掉得到的图片URL中的转义字符'\\'
                imageUrl = item.replace("\\", "")
                allImageUrl.append(imageUrl)

def save(text, path='download'):
    fpath = os.path.join(path,str(time.time()))
    with open(fpath, 'wb+') as  f:
        print('output:', fpath)
        f.write(text)

def save_image(image_url):
    resp = requests.get(image_url)
    page = resp.content
    filename = image_url.split('zhimg.com/')[-1]
    save(page)

def saveImagesFromUrl():
    path = os.path.join('download')
    imagesUrl = getImageUrl()
    print ("图片数: ", len(imagesUrl))
    if not imagesUrl:
        print ('imagesUrl is empty')
        return
    nameNumber = 0;
    for image in imagesUrl:
        suffixNum = image.rfind('.')
        suffix = image[suffixNum:]
        fileName = path + os.sep + suffix
        nameNumber += 1
        save_image(image)
    print ('图片下载完毕')

saveImagesFromUrl()
