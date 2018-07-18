# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:48:27 2018

@author: ShangFR
"""
import pandas as pd
import numpy as np
import tushare as ts



#缺失值处理
def my_na(stocks_df):
    stocks_df = stocks_df.drop_duplicates()
    col = list(set(stocks_df.select_dtypes(include=['float64','int']).columns))
#col_type = stocks_df.dtypes
    for i in col:
        na_per = stocks_df[i].isnull().sum()/len(stocks_df[i])
        if na_per < 0.3:         # 缺失值小于30%
            med = np.median(stocks_df[i].dropna())#中位数
            stocks_df.loc[:,i] = stocks_df.loc[:,i].fillna(med)#中位数填充缺失值
        else:
            stocks_df.loc[:,i] = stocks_df.loc[:,i].fillna(0)#用0填充缺失值
            med = np.median(stocks_df[i].dropna())#中位数
    return stocks_df

#获取沪深上市公司基本情况。
stocks_basics = ts.get_stock_basics()
stocks_basics["code"] = stocks_basics.index
#获取2018年第1季度的业绩报表数据
stocks_report = ts.get_report_data(2018,1)
#获取2018年第1季度的盈利能力数据
stocks_profit = ts.get_profit_data(2018,1)
#获取2018年第1季度的营运能力数据
stocks_operation = ts.get_operation_data(2018,1)
#获取2018年第1季度的成长能力数据
stocks_growth = ts.get_growth_data(2018,1)
#获取2018年第1季度的偿债能力数据
stocks_debtpaying = ts.get_debtpaying_data(2018,1)
#获取2018年第1季度的现金流量数据
stocks_cashflow = ts.get_cashflow_data(2018,1)

hs300 = ts.get_hs300s()

#处理缺失值
stocks_basics = my_na(stocks_basics)
stocks_report = my_na(stocks_report)
stocks_profit = my_na(stocks_profit)
stocks_operation = my_na(stocks_operation)
stocks_growth = my_na(stocks_growth)
stocks_debtpaying = my_na(stocks_debtpaying)
stocks_cashflow = my_na(stocks_cashflow)
hs300 = my_na(hs300)

hs300.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/hs300s.csv", float_format = '%.2f',encoding='utf-8',index=0)
stocks_basics.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_basics.csv", float_format = '%.2f',encoding='utf-8',index=0)
stocks_report.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_report.csv", float_format = '%.2f',encoding='utf-8',index=0)
stocks_profit.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_profit.csv", float_format = '%.2f',encoding='utf-8',index=0)
stocks_operation.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_operation.csv", float_format = '%.2f',encoding='utf-8',index=0)
stocks_growth.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_growth.csv", float_format = '%.2f',encoding='utf-8',index=0)
stocks_debtpaying.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_debtpaying.csv", float_format = '%.2f',encoding='utf-8',index=0)
stocks_cashflow.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_cashflow.csv", float_format = '%.2f',encoding='utf-8',index=0)


#行业划分：非金融上市公司、证券、银行、保险
#stocks_industry
stocks = stocks_basics.loc[:, ["code","industry"]]
stocks.loc[np.logical_not(stocks['industry'].isin(["银行","证券","保险"])), "industry"] = "非金融"# np.logical_not 代表not isin
stocks['industry'].value_counts()

#level 评级函数
def level(x):
    return sum(x)/len(x)

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
            ins_df.loc[ins_df[j] <= Q0,j+"_Q"]= 1
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
stocks_level.to_csv("C:/Users/ShangFR/Desktop/tushare/csvdata/stocks_level.csv", float_format = '%.2f',encoding='utf-8',index=0)




