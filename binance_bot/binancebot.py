import ccxt
import pandas as pd
import time
pd.set_option('display.max_rows', 5000)

exchange = ccxt.binance({'apiKey':'xxx','secret':'xxx'})
#balance = exchange.private_get_account()
#df = pd.DataFrame(balance['balances'])
symbol = 'XRPUSDT'
quantity = 20
price = 0.3000

print(exchange.fapiPrivateV2_get_balance({'timestamp':int(time.time()*1000)}))

#交易
'''print(exchange.fapiPrivate_post_order(
	params = {'symbol':symbol,'quantity':quantity,'price':price,'newClientOrderId':'TEST001','side':'BUY','type':'LIMIT','timeInForce':'GTC','timestamp':int(time.time()*1000)}
	))'''

#查询订单
#if exchange.fapiPrivate_get_order({'symbol':symbol,'origClientOrderId':'TEST001','timestamp':int(time.time()*1000)})['status'] == 'FILLED':

#获取&改变仓位模式
'''print(exchange.fapiPrivate_get_positionside_dual(
	params = {'timestamp': int(time.time()*1000)}
	))

exchange.private_post_order(
	params = {'symbol':symbol,'quantity':quantity,'price':price,'side':'BUY','type':'LIMIT','timeInForce':'GTC','timestamp':int(time.time()*1000)}
	)'''