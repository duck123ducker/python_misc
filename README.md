## 介绍
平时没事写的杂七杂八的python小脚本文件，大部分为高度定制化，没有注释，或许需要修改或安装模块才能满足你的需求。

### stock
stock_info.py是获取A股所有股票日线和周线行情的代码。

filter是根据日线计算macd等指标并判断是否金叉或达到特定条件的代码。

### kemono_downloader
kemono的特定作者所有作品（图片及视频下载链接）爬虫，其余文件需要自行修改代码。

### binance_bot
基于币安交易所的pythonsdk的量化交易机器人，内置策略适合单边行情，不适合震荡行情，可自行修改策略，曾取得两天20个点的成绩。

bot.py是主程序。

binancebot.py是接收实时行情并保存到本地以便日后回测策略的程序。

celvexxx.py是使用保存的过往行情数据回测某些策略的程序（经过回测，最后全部归零，炒币有风险，投资需谨慎）。

### ex_sharer
将exhentai的某个画廊的所有图片下载在自己服务器上，将它们拼接为一张长图并生成二维码和markdown文件，二维码中链接利用notion的域名做保护，可以直接在qq中扫码阅读，而不会被腾讯拦截。本程序高度定制化，需要先用nginx或apache设置好对相应文件夹的访问权限。
在使用之前需要先设置好cookie并且上传两个字体文件到当前工作文件夹中，名字分别为：`font_jp.ttf`和`font.ttf`，分别用作二维码中的画廊标题和自定义大标题。

### telegraph_downloader
下载通过telegra.ph分享的画廊。
