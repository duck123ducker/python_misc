import requests
import re
import math
import os
import qrcode
import threading
from PIL import Image, ImageFont, ImageDraw

baseurl = "https://exhentai.org/"
cookie = "xxx"
mySiteDomain = "xxx.xxx.com"
headers = {"Host": "exhentai.org","Connection": "close","Cache-Control": "max-age=0","sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"","sec-ch-ua-mobile": "?0","sec-ch-ua-platform": "\"Windows\"","Upgrade-Insecure-Requests": "1","DNT": "1","User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "navigate","Sec-Fetch-User": "?1","Sec-Fetch-Dest": "document","Referer": "https://exhentai.org/?f_cats=767&advsearch=1&f_sname=on&f_stags=on&f_sr=on&f_srdd=5","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9,de;q=0.8,ja;q=0.7,zh-TW;q=0.6","Cookie": cookie}
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

class myThread (threading.Thread):
    def __init__(self, page, path):
        threading.Thread.__init__(self)
        self.page = page
        self.path = path
    def run(self):
        counts=-1
        while True:
            if counts==4:#重试次数
                break
            try:
                print ("开启线程： " + self.path)
                with open(str(self.path) , 'wb') as f:
                    f.write(requests.get(self.page, headers=headers, proxies=proxies,timeout=(60, 60)).content)
                break
            except Exception as e:
                print(repr(e))
                counts+=1


def w_f_list( file_save , raw ):
    with open(file_save, "w", encoding='utf-8') as file:#存入新信息
        for content in raw:
            file.write(str(content) + '\n')

def make_qrcode(img_content, text):
    #count = 16#每行字数
    texts = text.split('\n')
    font = ImageFont.truetype(font='font_jp.ttf', size=24)
    st = 0#计算单行内字符
    lines = []
    for index in range(len(texts[1])):
        if index + 1 != len(texts[1]):
            width, height = font.getsize(texts[1][st:index+2])
            if width > 380:
                lines.append(texts[1][st:index+1])
                st = index + 1
    lines.append(texts[1][st:])
    line = len(lines)
    im = Image.new("RGB", (400, 430 + line*24), (255,255, 255))
    img = qrcode.make(img_content).convert("RGB").resize((400, 400), Image.ANTIALIAS)
    im.paste(img, (0, 30 + line * 24))
    dr = ImageDraw.Draw(im)
    width, height = ImageFont.truetype(font='font.ttf', size=32).getsize(texts[0])#计算标题居中
    dr.text((200-width/2, 5), texts[0], font=ImageFont.truetype(font='font.ttf', size=32), fill="#000000")
    for index in range(len(lines)):
        dr.text((10, 49 + index * 24), lines[index], font=font, fill="#000000")
    return im

def join(paths, out):
    '''
    :param png1: path
    :param png2: path
    :param flag: horizontal or vertical
    :return:
    '''
    imgs = []
    sizes = []
    for index in range(len(paths)):
        text = str(index + 1) + "/" + str(len(paths))
        im = Image.new("RGB", (1280, 100), (0, 0, 0))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(font='font.ttf', size=60)
        dr.text((600, 10), text, font=font, fill="#FFFFFF")
        imgs.append(im)
        sizes.append((1280, 100))

        img = Image.open(paths[index])
        size = img.size
        if size[0] != 1280:
            size = (1280, round(size[1] * 1280 / size[0]))
            img = img.resize(size, Image.ANTIALIAS)
        imgs.append(img)
        sizes.append(size)
    sizes_map = []#下面都是为了分割jpg最长65535像素的乱七八糟的shit
    imgs_map = []
    st = 0
    length = 0
    for index in range(len(sizes)):
        length = length + sizes[index][1]
        if index + 1 != len(sizes):
            if length + sizes[index + 1][1] + 1380 > 65500:
                sizes_map.append(sizes[st:index + 1])
                imgs_map.append(imgs[st:index + 1])
                st = index + 1
                length = 0
    sizes_map.append(sizes[st:])
    imgs_map.append(imgs[st:])
    for index in range(len(sizes_map)-1, -1, -1):
        if index + 1 != len(sizes_map):
            text = '达到长图最大限制，扫码翻页'
            im = Image.new("RGB", (1280, 100), (0, 0, 0))
            dr = ImageDraw.Draw(im)
            font = ImageFont.truetype(font='font.ttf', size=60)
            dr.text((300, 10), text, font=font, fill="#FFFFFF")
            #imgs_map[index] = [im] + imgs_map[index]
            #sizes_map[index] = [(1280, 100)] + sizes_map[index]
            imgs_map[index].append(im)
            sizes_map[index].append((1280, 100))
            img = qrcode.make(r'https://www.notion.so/image/http%3A%2F%2F'+mySiteDomain+'%3A12333%2F' + out[14:] + r'%2Fout___' + str(index + 2) + '.jpg?width=1280').convert("RGB").resize((1280,1280), Image.ANTIALIAS)
            #imgs_map[index] = [img] + imgs_map[index]
            #sizes_map[index] = [(1280, 1280)] + sizes_map[index]
            imgs_map[index].append(img)
            sizes_map[index].append((1280, 1280))
        length = 0
        for size in sizes_map[index]:
            length = length + size[1]
        joint = Image.new('RGB', (sizes_map[index][0][0], length))
        loc = (0, 0)
        for index_1 in range(len(sizes_map[index])):
            joint.paste(imgs_map[index][index_1], loc)
            loc = (0, loc[1] + sizes_map[index][index_1][1])
        joint.save(out + '/out___' + str(index + 1) + '.jpg', quality=85)
    return 'jpg'

def getpage(id):
    ids = id.split('/')
    response = (requests.get(baseurl + id, headers=headers, proxies=proxies).text)
    try:
        num = re.search(r'((?<=Showing 1 - [0-9] of )[0-9]{1,4}(?= images))|((?<=Showing 1 - [0-9][0-9] of )[0-9]{1,4}(?= images))',response).group() #图片数量
    except:
        num = re.search(r'((?<=Showing 1 - [0-9][0-9][0-9] of )[0-9]{1,4}(?= images))',response).group()  # 图片数量
    pages = re.findall(r'https://exhentai.org/[a-z]/[a-zA-Z0-9]{4,20}/' + ids[1] + '-[0-9]{1,4}', response) #图片详细链接
    p = math.ceil(int(num)/100)#页数
    for index in range(1,p,1):#页数>=2时生效
        response = (requests.get(baseurl + id + '?p=' + str(index), headers=headers, proxies=proxies).text)
        pages = pages + re.findall(r'https://exhentai.org/[a-z]/[a-zA-Z0-9]{4,20}/' + ids[1] + '-[0-9]{1,4}', response)
    name = re.search(r'(?<=<h1 id="gj">).*(?=</h1>)',response).group()
    if name == '':
        name = re.search(r'(?<=<h1 id="gn">).*(?=</h1><h1 id="gj">)',response).group()
    return pages, name

def getlink(page):
    response = (requests.get(page, headers=headers, proxies=proxies).text)
    link = re.search(r'((?<=<img id="img" src=")https://.*?\.jpg(?=" style="))|((?<=<img id="img" src=")https://.*?\.png(?=" style="))', response)
    if link is not None:
        link = link.group()
    return link

if __name__ == "__main__":
    content = '/createmd g/2347953/a4d0dd46cd/2600_1'
    mess = re.search(r'(?<=/createmd ).*', content).group().split('/')
    id = mess[0] + '/' + mess[1] + '/' + mess[2] + '/'
    dir = 'db/' + mess[3] + '_' + re.sub('/', '_', id)
    pages, name = getpage(id)
    links = []
    paths = []
    pass_bool = True
    try:
        os.mkdir(dir)
    except:
        pass_bool = False
    if pass_bool:
        threads = []
        for index in range(len(pages)):
            path = dir + '/' + str(index) + '.jpg'
            link = getlink(pages[index])
            print(index)
            if link is not None:
                links.append(link)
                paths.append(path)
            t = myThread(link, path)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    else:
        for index in range(len(pages)):
            path = dir + '/' + str(index) + '.jpg'
            paths.append(path)
            '''with open(paths[index], 'wb') as f:
                f.write(requests.get(link, headers=headers, proxies=proxies).content)
                print(paths[index])'''
    """先获取链接再下载改为边获取链接边下载
    for index in range(len(links)):
        # name = re.search(r'([^/]+)/?$', link).group()
        with open(path, 'wb') as f:
            f.write(requests.get(links[index], headers=headers).content)
    """
    # 下载完毕，生成长图
    form = join(paths, dir)
    img = make_qrcode(
        r'https://www.notion.so/image/http%3A%2F%2F'+mySiteDomain+'%3A12333%2F' + dir[14:] + r'%2Fout___1.' + form+'?width=1280',mess[3] + '\n' + name)
    img.save(dir + "/qrcode.jpg")
    contents_md = ['**<center>' + id + '**']
    contents_html = ['<h3 align="center">' + id + '</h3>']
    for index in range(len(links)):
        paths[index] = 'https://'+mySiteDomain+'/test' + paths[index]
        contents_md.append('<center>' + str(index + 1) + '/' + str(len(links)) + '\n')
        contents_md.append('![' + str(index) + '.jpg](' + paths[index] + ')')
        contents_html.append('<div align="center">' + str(index + 1) + '/' + str(len(links)) + '</div>\n')
        contents_html.append('<img src="' + paths[index] + '" />')
    w_f_list(dir + '/md.txt', contents_md)
    w_f_list(dir + '/html.txt', contents_html)