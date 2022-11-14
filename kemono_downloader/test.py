import threading
import requests

headers = {"Host": "data28.kemono.party", "Connection": "keep-alive", "DNT": "1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9,de;q=0.8,ja;q=0.7,zh-TW;q=0.6"}


proxies = {'https': 'http://127.0.0.1:7890', 'http':'http://127.0.0.1:7890'}

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        content = requests.get("https://data28.kemono.party/data/59/c7/59c7f50fedc69fb3862c60537d2a1ddd5489ae1a0120abbbfce03d4e060c9784.jpg?f=c41b1af9-0ad7-4346-a3c1-40e0db73a2c4.jpg", headers=headers, proxies = proxies).content
        if len(str(content)) != 9082912:
            print(str(content))


threads = []
for i in range(100):
    t = myThread()
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()