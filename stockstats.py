# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 10:18:45 2018

@author: ShangFR
"""

import math
import pandas as pd
import numpy as np
import tushare as ts
import datetime
import matplotlib.pyplot as plt
import stockstats

begin_time = '2018-02-01'
end_time = '2018-7-01'
code = "000001"
stock = ts.get_hist_data(code, start=begin_time, end=end_time)
stock["date"] = stock.index.values #增加日期列。
stock = stock.sort_index(0) # 将数据按照日期排序下。
#print(stock) [186 rows x 14 columns]
#初始化统计类
#stockStat = stockstats.StockDataFrame.retype(pd.read_csv('002032.csv'))
stockStat = stockstats.StockDataFrame.retype(stock)
print("init finish .")

# volume delta against previous day 
# The Volume Delta (Vol ∆) 
#返回数量。
# close price less than 10.0 in 5 days count
print(stockStat['close_10.0_le_5_c'].tail())

stockStat['kdjk_3_xu_kdjd_3']

#返回 True False 可以作为是否购买结果。
# CR MA2 cross up CR MA1 in 20 days count
print(stockStat['cr-ma2_xu_cr-ma1_20_c'].tail()) 
#交易量的delta转换。交易量是正，volume_delta把跌变成负值。
stockStat[['close','close_delta']].plot(subplots=True, figsize=(20,10), grid=True)
plt.show()



stockStat[
    ['close','close_1_d','close_2_d','close_-1_d','close_-2_d']
         ].plot(subplots=True, figsize=(20,10), grid=True)
plt.show()
# close_1_d  1 天的价差。 n天 - (n+1)天
# close_2_d  1 天的价差。 n天 - (n+2)天
# shift 函数是将数据 向前-n 向后+n 移动n天。 但是这个操作做了一个负值。
# 也就是 close_-1_d 才是和昨天的差 close_1_d 是和明天的差
#print(stockStat['close_-2_d'].head(10))
#print("stockStat['close']-stockStat['close'].shift(-1)")
#print((stockStat['close']-stockStat['close'].shift(-2)).head(10))
#print("############检查数据")
#print(stockStat['close'].head(10))
#print(stockStat['close'].shift(2).head(10))


stockStat[
    ['close','close_-1_r','close_-2_r']
         ].plot(subplots=True, figsize=(20,10), grid=True)
plt.show()


# CR indicator, including 5, 10, 20 days moving average
stockStat[
    ['cr','cr-ma1','cr-ma2','cr-ma3']
         ].plot(figsize=(20,10), grid=True)
plt.show()



stockStat[['kdjk','kdjd','kdjj'] # 分别是k d j 三个数据统计项。
         ].plot(figsize=(20,10), grid=True)
plt.show()


stockStat[['close','macd','macds','macdh'] #
         ].plot(subplots=True,figsize=(20,10), grid=True)
plt.show()