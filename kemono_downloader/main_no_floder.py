import requests
import re

proxies = {'https': '', 'http':''}
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
    links = re.findall(r'(?<=<a class="fileThumb" href=")/data/.*(?=">)', response)  # 图片详细链接
    for index in range(len(links)):
        links[index] = baseurl + links[index]
    print(links[1:])
    return links[1:]

def download(links):
    failed = []
    for index in range(len(links)):
        print(index)
        real_link = requests.get(links[index][1], headers=img_headers, allow_redirects=False, proxies = proxies).headers['Location']
        headers = real_img_headers
        host = re.search(r'(?<=https://).*(?=/data/)',real_link).group()
        headers["Host"] = host
        with open(dir + str(links[index][0]) + real_link.split('.')[-1], 'wb') as f:
            img = requests.get(real_link, headers=headers, proxies = proxies).content
            if "DDoS" in str(img):
                failed.append(links[index])
                print(failed)
            else:
                f.write(img)
    print(failed)
    return failed

if __name__ == '__main__':
    pages = []
    links = []
    pages = ['https://beta.kemono.party/fantia/user/13196/post/1365338']
    '''for i in range(0,376,25):#跟据页码调整
        print(i)
        pages = pages + getpage('https://beta.kemono.party/fantia/user/xxxxx?o=' + str(i))
    print(len(pages))'''
    for page in pages:
        link = getlink(page)
        links = links + link
    #批量图片下载
    for index in range(len(links)):
        links[index] = (index, links[index])
    while len(links) != 0:
        links = download(links)