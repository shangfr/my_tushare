# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 11:13:43 2018

@author: ShangFR
"""

import tushare as ts
import jieba
import jieba.analyse
import pandas as pd

jieba.load_userdict("C:/Users/ShangFR/Desktop/tushare/dict/user.dict.utf8")
sell=pd.read_csv('C:/Users/ShangFR/Desktop/tushare/dict/sell.csv',encoding='gb2312')
buy=pd.read_csv('C:/Users/ShangFR/Desktop/tushare/dict/buy.csv',encoding='gb2312')

codes=["603277","300700","603063","300027"]
notices = {}
for i in codes:
    notices[i] = ts.get_notices(code=i)
    notices[i]["analys"] = 0 
    for j in range(30):
        testfile = ts.notice_content(notices[i]["url"][j])  
        testfile = testfile.replace(' ','').replace('\r\n','')#去除空格#.split("\n") \n切分
        seg_list = jieba.cut(testfile)
        print(type(seg_list))
        #词频统计
        word_Series = pd.Series(list(seg_list))
        word_df = word_Series.value_counts().to_frame(name="freq")
        word_df["key"] = word_df.index
        #提取关键词
        sell_freq = pd.merge(left=word_df, right=sell, how='inner', left_on='key', right_on='key')
        buy_freq = pd.merge(left=word_df, right=buy, how='inner', left_on='key', right_on='key')
        analys = sum(buy_freq["freq"]*buy_freq["weight"]) - sum(sell_freq["freq"]*sell_freq["weight"])
    notices[i].loc[0,"analys"]=analys 







keywords = jieba.analyse.extract_tags(testfile, topK=20, withWeight=True, allowPOS=('n','nr','ns'))

print(type(keywords))
for item in keywords:
    print(item[0],item[1])






news = ts.get_latest_news(top=5,show_content=True)
#news = ts.latest_content(news["url"][1])

import wordcloud as wc
import matplotlib.pyplot as plt   
# 引入字体
font=r"C:/Users/ShangFR/Desktop/tushare/Fonts/simsun.ttc"

# 生成词云对象，设置参数
cloud = wc.WordCloud( font_path=font,#设置字体
           background_color='white', #背景颜色
           max_words=2000,# 词云显示的最大词数
           #mask=color_mask,#设置背景图片
           max_font_size=100, #字体最大值
           random_state=30,
           scale=3.5)
# 绘制词云图
plt.figure(figsize=(160,90))
plt.ion()
news = ts.get_latest_news(top=10,show_content=True)
try:
    i = 0
    while i < 10:
        mywc = cloud.generate(news["content"][i])
        plt.imshow(mywc)
        plt.axis("off")
        plt.show()
        plt.pause(5)
        if i > 8:     # 当i大于10时跳出循环
            news = ts.get_latest_news(top=10,show_content=True)
            i = 0
        else:
            i = i + 1
    else:
        print("结束")
except KeyboardInterrupt:
    plt.close()
    print("退出")
    pass
