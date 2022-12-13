import time
import ccxt
import logging
from binance.lib.utils import config_logging
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

def get_beijin_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time.time() + 28800))

def w_f( file_save , raw ):
    with open(file_save, "a", encoding='utf-8') as file:#存入新信息
        file.write(str(raw) + '\n')

def getbalance():
    try:
        responses = exchange.fapiPrivateV2_get_balance({'timestamp':int(time.time()*1000)})
        for response in responses:
            if response['asset'] == 'USDT':
                balance = float(response['availableBalance'])
                mess = get_beijin_time() + ' ' + str(balance)
                print(mess)
                w_f('balancelog.txt', mess)
                return balance
    except:
        return getbalance()


exchange = ccxt.binance({'apiKey':'xxx','secret':'xxx'})
api_key = "xxx"
config_logging(logging, logging.INFO)
pr = [] #存储价格
bpr = 0 #成交价
position = getbalance() #头寸（起始资金）
quantity = 0 #订单数量
position_sta = 0 #0:空仓;1:buy空仓;2:short空仓;3:filled买;4:filled做空;5:long满仓;6:sell满仓
symbol = 'ADAUSDT'

def sell(pr,sta):#sta=1:sell;sta=2:short
    global position_sta,quantity
    oldsta = position_sta
    try:
        if sta == 1: #sell
            position_sta = 6 #sell满仓
        if sta == 2: #short
            quantity = round(2*position/pr, 0)
            position_sta = 2 #short空仓
        exchange.fapiPrivate_post_order(params = {'symbol':symbol,'quantity':quantity,'side':'SELL','type':'MARKET','timestamp':int(time.time()*1000)})
    except Exception as e:
        position_sta = oldsta
        print(repr(e))


def buy(pr,sta):#sta=1:buy;sta=2:long
    global position_sta,quantity
    oldsta = position_sta
    try:
        if sta == 1: #buy
            quantity = round(2*position/pr, 0)
            position_sta = 1 #buy空仓
        if sta == 2: #long
            position_sta = 5 #long满仓
        exchange.fapiPrivate_post_order(params = {'symbol':symbol,'quantity':quantity,'side':'BUY','type':'MARKET','timestamp':int(time.time()*1000)})
    except Exception as e:
        position_sta = oldsta
        print(repr(e))

def info_handler(message):
    global order_sta,position_sta,bpr,quantity,position
    if 'e' in message.keys():
        if message['e'] == 'ORDER_TRADE_UPDATE':
            if message['o']['X'] == 'NEW':
                pass
            if message['o']['X'] == 'FILLED':
                mess = ''
                if position_sta == 1:
                    position_sta = 3
                    mess = get_beijin_time() + ' buy at ' + str(message['o']['ap'])
                elif position_sta == 2:
                    position_sta = 4
                    mess = get_beijin_time() + ' sell at ' + str(message['o']['ap'])
                elif (position_sta == 5) | (position_sta == 6):
                    position = getbalance() #更新头寸
                    position_sta = 0
                    mess = get_beijin_time() + ' close out at ' + str(message['o']['ap'])
                bpr = float(message['o']['ap']) #更新成交价格
                quantity = message['o']['q'] #更新仓位
                print(mess) #输出交易信息
                w_f('balancelog.txt', mess)

def ticker_handler(message): #每秒触发
    global bpr
    if 'c' in message.keys():
        if len(pr) < 20: #10秒内价格
            pr.append(float(message['c']))
        else:
            del pr[0]
            pr.append(float(message['c']))
            if position_sta == 0: #若空仓且无挂单
                opr = sum(pr[0:10])/5
                npr = sum(pr[10:20])/5
                if npr < opr:
                    sell(pr[19],2) #做空
                elif npr > opr: #价格高
                    buy(pr[19],1) #买
            elif (position_sta == 3) | (position_sta == 4): #全仓
                point = (pr[19]-bpr)/bpr
                #point1 = "%.3f%%" % (point * 100)
                #print(get_beijin_time() + ' ' + point1)
                if (point <= -0.005) & (position_sta == 3): #做多仓亏0.5个点
                    sell(pr[19],1) #卖
                #elif ((point <= -0.01) & (position_sta == 4)) | ((point >= 0.01) & (position_sta == 3)): #做空仓赚一个点OR做多仓赚一个点
                elif ((pr[19] < bpr) & (position_sta == 4)) | ((pr[19] > bpr) & (position_sta == 3)): #最高价格更新
                    bpr = pr[19] #更新成本价（省手续费）
                elif (point >= 0.01) & (position_sta == 4): #做空仓亏0.5个点
                    buy(pr[19],2) #买平


client = UMFutures(api_key)
response = client.new_listen_key()
logging.info("Listen key : {}".format(response["listenKey"]))
ws_client = UMFuturesWebsocketClient()
ws_client.start()
ws_client.user_data(listen_key=response["listenKey"],id=1,callback=info_handler)
ws_client.mini_ticker(id=2, callback=ticker_handler, symbol="adausdt")
while True:
    print(get_beijin_time() + ' renew ' + str(exchange.fapiPrivatePutListenKey()))
    time.sleep(600)
logging.debug("closing ws connection")
ws_client.stop()