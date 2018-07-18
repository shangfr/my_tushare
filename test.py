# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 10:40:33 2018

@author: ShangFR
"""

import tushare as ts
import pandas as pd
import numpy as np
top_list = ts.top_list('2018-07-12')
cap_tops = ts.cap_tops()
inst_tops = ts.inst_tops()
broker_tops = ts.broker_tops()

codes=["603277","300700","603063","300027"]
dates=['2018-7-10','2018-7-11','2018-7-12','2018-7-13']
df=pd.DataFrame()

for code in codes:
    for date in dates:
        df1 = ts.get_sina_dd(code, date, vol=400)  #指定大于等于400手的数据
        if df1 is None:
            df = df
        else:
            df1["date"] = date
            df = pd.concat([df,df1],axis=0) 

df["amount"] = df["volume"] * df["preprice"] 

sum(df.loc[df["type"].isin(["买盘","中性盘"]),"amount"])

    


import matplotlib.pyplot as plt
import numpy as np



#概率分布直方图
x0= df.loc[df["type"].isin(["卖盘"]) & df["date"].isin(['2018-7-10']),"amount"]
x1= df.loc[df["type"].isin(["卖盘"])& df["date"].isin(['2018-7-11']),"amount"]
x2= df.loc[df["type"].isin(["卖盘"]) & df["date"].isin(['2018-7-12']),"amount"]
x3= df.loc[df["type"].isin(["卖盘"])& df["date"].isin(['2018-7-13']),"amount"]


fig = plt.figure(figsize=(16,9))
ax0 = fig.add_subplot(421)
ax1 = fig.add_subplot(422)
ax2 = fig.add_subplot(423)
ax3 = fig.add_subplot(424)
ax4 = fig.add_subplot(425)
ax5 = fig.add_subplot(426)
ax6 = fig.add_subplot(427)
ax7 = fig.add_subplot(428)
#第二个参数是柱子宽一些还是窄一些，越大越窄越密
ax0.hist(x0,100,normed=1,histtype='bar',facecolor='yellowgreen',alpha=0.75)
##pdf概率分布图，一万个数落在某个区间内的数有多少个
ax0.set_title('pdf')
ax1.hist(x0,100,normed=1,histtype='bar',facecolor='pink',alpha=0.75,cumulative=True,rwidth=0.8)
#cdf累计概率函数，cumulative累计。比如需要统计小于5的数的概率
ax1.set_title("cdf")

ax2.hist(x1,100,normed=1,histtype='bar',facecolor='yellowgreen',alpha=0.75)
ax2.set_title('pdf1')
ax3.hist(x1,100,normed=1,histtype='bar',facecolor='pink',alpha=0.75,cumulative=True,rwidth=0.8)
ax3.set_title("cdf1")

ax4.hist(x2,100,normed=1,histtype='bar',facecolor='yellowgreen',alpha=0.75)
ax4.set_title('pdf1')
ax5.hist(x2,100,normed=1,histtype='bar',facecolor='pink',alpha=0.75,cumulative=True,rwidth=0.8)
ax5.set_title("cdf1")

ax6.hist(x3,100,normed=1,histtype='bar',facecolor='yellowgreen',alpha=0.75)
ax6.set_title('pdf1')
ax7.hist(x3,100,normed=1,histtype='bar',facecolor='pink',alpha=0.75,cumulative=True,rwidth=0.8)
ax7.set_title("cdf1")


fig.subplots_adjust(hspace=0.4)
plt.show()



ts.profit_data(top=10)
dd = ts.forecast_data(2018,2)

dd.type.value_counts()




import matplotlib.pyplot as plt 



ts.get_deposit_rate()
get_rrr = ts.get_rrr()
get_rrr = get_rrr.replace('--', 0)
df = get_rrr.iloc[:,1:4].astype(float)
df.index=get_rrr.date
df = df.sort_index()

ch = df.changed.cumsum()
ch.plot()
df.plot()



