import requests
import re

jpg_regex = r'<img src="/file/[^png]*?\.jpg"'
url = "https://telegra.ph/xxx"
proxy={"http":"http://127.0.0.1:7890","https":"http://127.0.0.1:7890"}
jpg_urls = re.findall(jpg_regex, requests.get(url,proxies=proxy).text)
jpg_links = []
for jpg_url in jpg_urls:
    link = jpg_url.split('"')[1]
    jpg_links.append("https://telegra.ph"+link)
print(jpg_links)
print(len(jpg_links))
MAX_RETRIES = 5
for index in range(len(jpg_links)):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            print(index)
            response = requests.get(jpg_links[index],proxies=proxy)
            open('db/'+('000'+str(index+1))[-3:]+".jpg", "wb").write(response.content)
            break
        except:
            retries += 1