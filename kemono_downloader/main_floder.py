# -*- coding:utf-8 -*-
import requests
import re
import os
import shutil
from lxml import etree

proxies = {'https': 'http://127.0.0.1:7890', 'http':'http://127.0.0.1:7890'}
baseurl = 'https://beta.kemono.party'
img_baseurl = 'https://data19.kemono.party'
headers = {"Host": "beta.kemono.party", "Connection": "keep-alive", "Cache-Control": "max-age=0", "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "DNT": "1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9,de;q=0.8,ja;q=0.7,zh-TW;q=0.6"}
img_headers = {"Host": "beta.kemono.party", "Connection": "keep-alive", "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "DNT": "1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9,de;q=0.8,ja;q=0.7,zh-TW;q=0.6"}
real_img_headers = {"Host": "", "Connection": "keep-alive", "DNT": "1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9,de;q=0.8,ja;q=0.7,zh-TW;q=0.6"}
dir = 'db/'
def getpage(page):
    response = (requests.get(page, headers=headers, proxies = proxies).text)
    pages = re.findall(r'/fantia/user/13196/post/.*(?=")', response) #帖子详细链接
    for index in range(len(pages)):
        pages[index] = baseurl + pages[index]
    return pages

def getlink(page):
    response = (requests.get(page, headers=headers, proxies = proxies).text)
    pic_links = re.findall(r'(?<=<a class="fileThumb" href=")/data/.*(?=">)', response)  # 图片详细链接
    for index in range(len(pic_links)):
        pic_links[index] = baseurl + pic_links[index]
    html = etree.HTML(response)
    file_links = html.xpath("//a[@class='post__attachment-link']/@href")
    for index in range(len(file_links)):
        file_links[index] = baseurl + file_links[index]
    name = html.xpath("//time[@class='timestamp ']/@datetime")[0].split(' ')[0] + '_' + html.xpath("//h1[@class='post__title']/span[1]/text()")[0]
    return {'name': name, 'pic_links': pic_links, "file_links": file_links}

def download(links):
    failed = []
    for index in range(len(links)):
        try:
            print(index)
            if not os.path.exists(dir + links[index][0].split('/')[0]):
                os.makedirs(dir + links[index][0].split('/')[0])
            real_link = requests.get(links[index][1], headers=img_headers, allow_redirects=False, proxies = proxies).headers['Location']
            headers = real_img_headers
            host = re.search(r'(?<=https://).*(?=/data/)',real_link).group()
            headers["Host"] = host

            with open(dir + str(links[index][0]), 'wb') as f:
                content = requests.get(real_link, headers=headers, proxies = proxies).content
                print(len(str(content)))
                if "DDoS" in str(content):
                    f.write(content)
                    #failed.append(links[index])
                    #print(failed)
                else:
                    f.write(content)
        except:
            failed.append(links[index])
            print(failed)
    print(failed)
    return failed

if __name__ == '__main__':
    pages = []
    links = []
    for i in range(0,376,25):#跟据页码调整
        print(i)
        pages = pages + getpage('https://beta.kemono.party/fantia/user/XXXXXX?o=' + str(i))#此处填入你的链接
    print(len(pages))

    for page in pages:
        result = getlink(page)
        for index in range(len(result['pic_links'])):
            links.append((result['name'] + '/' + str(index) + '.' + result['pic_links'][index].split('.')[-1], result['pic_links'][index]))
        for index in range(len(result['file_links'])):
            links.append((result['name'] + '/' + result['file_links'][index].split('=')[-1], result['file_links'][index]))
    print(links)

    while len(links) != 0:
        links = download(links)