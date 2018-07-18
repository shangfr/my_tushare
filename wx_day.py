# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 17:31:29 2018

@author: ShangFR
"""

import pandas as pd
import json

codes=["603277","300700","603063","300027"]

#获取沪深上市公司基本情况
stocks_basics = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_basics.csv", dtype = {'code' : str},encoding='utf-8')

#保存推荐股票的基本信息（json格式）
len(set(codes)-set(stocks_basics.code.tolist())) #检查codes是否存在
stock_index = stocks_basics.loc[stocks_basics.code.isin(codes)]
url = 'C:/Users/ShangFR/Desktop/tushare/jsondata/stocks_index.json'
stock_index_json = stock_index.to_json(orient='records', force_ascii=False)
fh = open(url, 'w', encoding='utf-8')
fh.write(stock_index_json)
fh.close()

stocks_level = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_level.csv",encoding='utf-8',dtype = {'code' : str})
len(set(codes)-set(stocks_level.code.tolist())) #检查codes是否存在
stock_level = stocks_level.loc[stocks_level.code.isin(codes)]
stock_level.index=stock_level["code"]

#获取各股评级  
stock_level_dict = stock_level.T.to_dict(orient='list')    
stock_level_json = json.dumps(stock_level_dict, ensure_ascii=False)   
url = 'C:/Users/ShangFR/Desktop/tushare/jsondata/stocks_level.json'
fh = open(url, 'w', encoding='utf-8')
fh.write(stock_level_json)
fh.close()


#获取各股实时行情
import tushare as ts
stocks_today = ts.get_today_all()
stocks_today.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stock_today_all.csv", float_format = '%.2f',encoding='utf-8',index=0)

stock_today = stocks_today.loc[stocks_today.code.isin(codes)]
stock_today.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stock_today.csv", float_format = '%.2f',encoding='utf-8',index=0)
stock_today = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stock_today.csv",encoding='utf-8',dtype = {'code' : str})
stock_today.index=stock_today["code"]


#stock_today.dtypes 
stock_today_json = stock_today.to_json(orient='index', force_ascii=False)
url = 'C:/Users/ShangFR/Desktop/tushare/jsondata/stocks_today.json'
fh = open(url, 'w', encoding='utf-8')
fh.write(stock_today_json)
fh.close()

import datetime
date = datetime.date.today()

#stocks_describe = stocks_today.describe()
#describe = stocks_describe[['changepercent',"open","settlement","turnoverratio","amount"]].loc[["mean","50%"]]
#my_zhishu = describe.apply(lambda x : x[0]/x[1], axis=0)
#zhishu = "%.1f" % (sum(my_zhishu)-5)

lst = stocks_today['changepercent']
len(lst)
intervals = {'{0}~{1}'.format( x*2 - 8, x*2 - 6 ): 0 for x in range(8)}
intervals['-11~-8']=0
intervals['8~11']=0
for _ in lst:
    for interval in intervals:
        start, end = tuple(interval.split('~'))
        if int(start) <= _ < int(end):
            intervals[interval] += 1

change_per = list(intervals.values())
rho =  list(range(0, 10))
zipped = zip(change_per,rho)     
prod = [a*b for a, b in zipped]
zhishu = round(sum(prod)/2500,1)


if zhishu>6:
    jianyi = "大盘走势良好，积极参与"
elif zhishu>5:
    jianyi = "大盘震荡整理，关注量能变化"
else:
    jianyi = "大盘震荡，适度参与"

 
 




getdpData = {'categories': ["T1", " ", "T3", " ", "T5", " ", "T7", " ","T9"],
 'data2': [4.07, -1.67, 1.26, -1.7, -1.36, -0.41, 0.71, -0.77,5.87],
 'data1': [-0.36, -2.23, -1.16, 0.26, -0.68, -3.86, -2.68, -4.18,3.8],
 'date': str(date),
 'jianyi': jianyi,
 'zhishu': zhishu}


getdpData_json = json.dumps(getdpData, ensure_ascii=False)  
stocks_index_json = '{"tuijian": %s}' % stock_index_json
wxjs_data = 'module.exports = { \n getdpData: function () { \n return %s},  \n getData: function () { \n  return %s}, \n getSTData: function () { \n return %s}, \n getTaData: function () { \n return %s }}' % (getdpData_json,stocks_index_json, stock_level_json, stock_today_json)
#保存成wx-js-data
fh = open('C:/Users/ShangFR/Desktop/本地简化版/utils/storage.js', 'w', encoding='utf-8')
fh.write(wxjs_data)
fh.close()

