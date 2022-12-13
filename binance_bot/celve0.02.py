#!/usr/bin/env python

import time
import logging
from binance.lib.utils import config_logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

config_logging(logging, logging.DEBUG)

pr = [] #存储价格
sta = 0
bpr = 0
usdt = 1000
btc = 0
btcb = 0
usdtb = 0

def w_f( file_save , raw ):
    with open(file_save, "a", encoding='utf-8') as file:#存入新信息
        file.write(str(raw) + '\n')

def logger(content):
    print(content)
    w_f('0.02.txt',content)

def get_beijin_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time.time() + 28800))

def sell(pr):
    global btc
    global usdt
    global btcb
    global usdtb
    global bpr
    global sta
    sta = 0
    usdt = btc*pr*0.9996 - usdtb
    usdtb = 0
    btc = 0
    bpr = 0
    logger(get_beijin_time() + ' sell at ' + str(pr))
    logger(get_beijin_time() + ' ' + str(usdt))

def buy(pr):
    global btc
    global usdt
    global btcb
    global usdtb
    global bpr
    global sta
    sta = 1
    usdtb = usdt
    btc = usdt*2/pr*0.9996
    usdt = 0
    bpr = pr
    logger(get_beijin_time() + ' buy at ' + str(pr))

def sell1(pr):
    global btc
    global usdt
    global btcb
    global usdtb
    global bpr
    global sta
    sta = 2
    btcb = usdt*2/pr
    usdt = usdt + usdt*2*0.9996
    bpr = pr
    logger(get_beijin_time() + ' short at ' + str(pr))

def buy1(pr):
    global btc
    global usdt
    global btcb
    global usdtb
    global bpr
    global sta
    sta = 0
    usdt = usdt - btcb*pr*1.0004
    btcb = 0
    bpr = pr
    logger(get_beijin_time() + ' long at ' + str(pr))
    logger(get_beijin_time() + ' ' + str(usdt))


def message_handler(message): #每秒触发
    global bpr
    if 'c' in message.keys():
        if len(pr) < 20: #10秒内价格
            pr.append(float(message['c']))
        else:
            del pr[0]
            pr.append(float(message['c']))
            opr = sum(pr[0:10])/5
            npr = sum(pr[10:20])/5
            if sta == 1: #已买
                point = (pr[19]-bpr)/bpr
                #point1 = "%.3f%%" % (point * 100)
                #print(point1 + ' ' + str(pr[19]))
                if point <= -0.02: #亏一个点
                    sell(pr[19]) #卖
                elif pr[19] > bpr: #最新价格大于历史最高点价格
                    bpr = pr[19]
            elif sta == 2: #已做空
                point = (pr[19]-bpr)/bpr
                #point1 = "%.3f%%" % (point * 100)
                #print(point1 + ' ' + str(pr[19]))
                if point >= 0.02: #亏一个点
                    buy1(pr[19]) #撤仓
                elif bpr > pr[19]:
                    bpr = pr[19]
            elif npr < opr:
                sell1(pr[19]) #做空
            elif npr > opr: #价格高
                buy(pr[19]) #买




my_client = UMFuturesWebsocketClient()
my_client.start()

my_client.mini_ticker(id=1, callback=message_handler, symbol="adausdt")   #监听行情


while 1:
    time.sleep(3000)

logging.debug("closing ws connection")
my_client.stop()
