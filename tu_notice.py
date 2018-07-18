# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:47:35 2018

@author: ShangFR
"""

import tushare as ts
import json

df = ts.get_industry_classified() #Single stock symbol
getTJData = df.loc[df['c_name'] =="环保行业"]
#构造字典
notices = {}
#获取各股公告  
for i in getTJData["code"]:
    notices[i] = ts.get_notices(code=i).to_dict(orient='records')
#ts.notice_content(ss["url"][0])    
notices_json = json.dumps(notices, ensure_ascii=False)   
url = 'C:/Users/ShangFR/Desktop/tushare/notices_json.json'
fh = open(url, 'w', encoding='utf-8')
fh.write(notices_json)
fh.close()



stocks = ts.get_stock_basics()
stocks['industry'].value_counts()

stocks.loc[stocks['industry'].isin(["银行","证券","保险"])]

lin = list(set(stocks['industry']))
getData = {}
for i in lin:
    df = stocks.loc[stocks['industry'] ==i]
    df_mean = df.iloc[:, 3:22].mean()
    level = df.iloc[:, 3:22]-df_mean
    df['level'] = level.apply(lambda x: x.sum(), axis=1)
    getData[i] = df.to_dict(orient='records')
    
    

getData.keys()

#getData["code"]=getData.index
url = 'C:/Users/ShangFR/Desktop/tushare/stocks_hb.json'
#stock_json = getData.to_json(orient='records', force_ascii=False)
stock_json = json.dumps(getData, ensure_ascii=False)   
fh = open(url, 'w', encoding='utf-8')
fh.write(stock_json)
fh.close()

#今日行业涨幅
stockData = ts.get_today_all()
stockData.to_csv("C:/Users/ShangFR/Desktop/tushare/TodayData.csv",encoding='utf-8',index=0)
lin = list(set(stockData['code']))

st = stockData.iloc[:, 0:3]
df = ts.get_industry_classified() 
import pandas as pd
inners = pd.merge(left=st, right=df, how='inner', left_on='code', right_on='code')
inners = inners.iloc[:, [2,4]]
lin = list(set(inners['c_name']))
df_mean = list()
for i in lin:
    ins = inners.loc[inners['c_name'] ==i]
    df_mean.append(ins.iloc[:, 0].mean())
    
pm = pd.DataFrame({"行业" : lin,"涨幅" : df_mean}) #将列表a，b转换成字典
pm.sort_values("涨幅")





# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 11:32:59 2018

@author: ShangFR
"""

import pandas as pd
import numpy as np
import json
#检测股票代码是否存在
#def my_code(stocks_df):
#stocks_df[np.logical_not(stocks_df["code"].isin(stocks["code"]))]



#缺失值处理
def my_na(stocks_df):
    stocks_df = stocks_df.drop_duplicates()
    col = list(set(stocks_df.select_dtypes(include=['float64','int']).columns))
#col_type = stocks_df.dtypes
    for i in col:
        na_per = stocks_df[i].isnull().sum()/len(stocks_df[i])
        if na_per < 0.3:         # 缺失值小于30%
            med = np.median(stocks_df[i].dropna())#中位数
            stocks_df[i] = stocks_df[i].fillna(med)#中位数填充缺失值
        else:
            stocks_df[i] = stocks_df[i].fillna(0)#用0填充缺失值
            med = np.median(stocks_df[i].dropna())#中位数
    return stocks_df

#推荐股票list
codes=["603227","300700","603063"]
#获取沪深上市公司基本情况
stocks_basics = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_basics.csv", dtype = {'code' : str},encoding='utf-8')
#6-df 业绩报告（主表）、盈利能力数据、营运能力数据、成长能力数据、偿债能力数据、现金流量数据
stocks_report = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_report.csv",encoding='utf-8',dtype = {'code' : str})
stocks_profit = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_profit.csv",encoding='utf-8',dtype = {'code' : str})
stocks_operation = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_operation.csv",encoding='utf-8',dtype = {'code' : str})
stocks_growth = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_growth.csv",encoding='utf-8',dtype = {'code' : str})
stocks_debtpaying = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_debtpaying.csv",encoding='utf-8',dtype = {'code' : str})
stocks_cashflow = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_cashflow.csv",encoding='utf-8',dtype = {'code' : str})

#处理缺失值
stocks_basics = my_na(stocks_basics)
stocks_report = my_na(stocks_report)
stocks_profit = my_na(stocks_profit)
stocks_operation = my_na(stocks_operation)
stocks_growth = my_na(stocks_growth)
stocks_debtpaying = my_na(stocks_debtpaying)
stocks_cashflow = my_na(stocks_cashflow)

#保存推荐股票的基本信息（json格式）
len(set(codes)-set(stocks_basics.code.tolist())) #检查codes是否存在
stock_index = stocks_basics.loc[stocks_basics.code.isin(codes)]
url = 'C:/Users/ShangFR/Desktop/tushare/stocks_index.json'
stock_json = stock_index.to_json(orient='records', force_ascii=False)
fh = open(url, 'w', encoding='utf-8')
fh.write(stock_json)
fh.close()

#stock_basics.dtypes


#行业划分：非金融上市公司、证券、银行、保险
#stocks_industry
stocks = stocks_basics.loc[:, ["code","industry"]]
stocks.loc[np.logical_not(stocks['industry'].isin(["银行","证券","保险"])), "industry"] = "非金融"# np.logical_not 代表not isin
stocks['industry'].value_counts()

#level 评级函数
def level(x):
    return sum(x)

def my_industry(stocks_df):
    stocks_df = pd.merge(left=stocks_df, right=stocks, how='inner', left_on='code', right_on='code')   
    lin = list(set(stocks_df['industry']))
    df_return = pd.DataFrame()
    for i in lin:
        ins_df = stocks_df.loc[stocks_df['industry'] ==i]
        ins_df = ins_df.drop_duplicates()
        col = list(set(ins_df.select_dtypes(include=['float64','int']).columns))
        for j in col:
            Q3 = np.percentile(ins_df[j],75)#95%分位数
            Q2 = np.median(ins_df[j].dropna())#中位数
            Q1 = np.percentile(ins_df[j],25)#95%分位数
            IQR = Q3-Q1
            Q4 = Q3+1.5*IQR
            Q0 = Q1-1.5*IQR
            Q0 = Q0 if Q0>0 else 0
            ins_df[j+"_Q"] = ins_df[j]
            ins_df.loc[ins_df[j] > Q4,j+"_Q"]= 6
            ins_df.loc[(ins_df[j] <= Q4) & (ins_df[j] > Q3) ,j+"_Q"]= 5
            ins_df.loc[(ins_df[j] <= Q3) & (ins_df[j] > Q2) ,j+"_Q"]= 4
            ins_df.loc[(ins_df[j] <= Q2) & (ins_df[j] > Q1) ,j+"_Q"]= 3
            ins_df.loc[(ins_df[j] <= Q1) & (ins_df[j] > Q0) ,j+"_Q"]= 2
            ins_df.loc[ins_df[j] <= Q0,j+"_Q"]= 0
        df_return = pd.concat([df_return,ins_df],ignore_index=True)
    df_return["level_Q"] = df_return[df_return.columns[df_return.columns.str.contains(r'.*?_Q.*')]].apply(level, axis=1)
    return df_return

#按行业分位数评级打分1-6分

stocks_report = my_industry(stocks_report)
stocks_profit = my_industry(stocks_profit)
stocks_operation = my_industry(stocks_operation)
stocks_growth = my_industry(stocks_growth)
stocks_debtpaying = my_industry(stocks_debtpaying)
stocks_cashflow = my_industry(stocks_cashflow)

#合并6个评分
stocks_level = stocks_basics.loc[:, ["code","name","industry"]]
stocks_level = pd.merge(left=stocks_level, right=stocks_report.loc[:, ["code","level_Q"]], how='left', left_on='code', right_on='code')   
stocks_level = pd.merge(left=stocks_level, right=stocks_profit.loc[:, ["code","level_Q"]], how='left', left_on='code', right_on='code')   
stocks_level = pd.merge(left=stocks_level, right=stocks_operation.loc[:, ["code","level_Q"]], how='left', left_on='code', right_on='code')   
stocks_level = pd.merge(left=stocks_level, right=stocks_growth.loc[:, ["code","level_Q"]], how='left', left_on='code', right_on='code')   
stocks_level = pd.merge(left=stocks_level, right=stocks_debtpaying.loc[:, ["code","level_Q"]], how='left', left_on='code', right_on='code')   
stocks_level = pd.merge(left=stocks_level, right=stocks_cashflow.loc[:, ["code","level_Q"]], how='left', left_on='code', right_on='code')   
     
stocks_level.columns=['code', 'name', 'industry', 'report', 'profit', 'operation','growth', 'debtpaying', 'cashflow']
stocks_level = my_na(stocks_level)
stocks_level.to_csv("C:/Users/ShangFR/Desktop/tushare/stocks_level.csv", float_format = '%.2f',encoding='utf-8',index=0)

stocks_level = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/stocks_level.csv",encoding='utf-8',dtype = {'code' : str})
len(set(codes)-set(stocks_level.code.tolist())) #检查codes是否存在
stock_level = stocks_level.loc[stocks_level.code.isin(codes)]
stock_level.index=stock_level["code"]

#获取各股评级  
stock_dict = stock_level.T.to_dict(orient='list')    
stock_json = json.dumps(stock_dict, ensure_ascii=False)   
url = 'C:/Users/ShangFR/Desktop/tushare/stocks_level.json'
fh = open(url, 'w', encoding='utf-8')
fh.write(stock_json)
fh.close()


#获取各股实时行情
import tushare as ts
stocks_today = ts.get_today_all()
stock_today = stocks_today.loc[stocks_today.code.isin(codes)]

stock_today.to_csv("C:/Users/ShangFR/Desktop/tushare/stock_today.csv", float_format = '%.2f',encoding='utf-8',index=0)
stock_today = pd.read_csv("C:/Users/ShangFR/Desktop/tushare/stock_today.csv",encoding='utf-8',dtype = {'code' : str})
stock_today.index=stock_today["code"]


#stock_today.dtypes 
stock_json = stock_today.to_json(orient='index', force_ascii=False)
url = 'C:/Users/ShangFR/Desktop/tushare/stocks_today.json'
fh = open(url, 'w', encoding='utf-8')
fh.write(stock_json)
fh.close()


































