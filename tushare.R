library(tidyverse)

library(cluster)
library(fpc)
stocks_basics <- read_csv("C:/Users/ShangFR/Desktop/tushare/stocks_basics.csv")
stocks_profit <- read_csv("C:/Users/ShangFR/Desktop/tushare/stocks_profit.csv")
TodayData <- read_csv("C:/Users/ShangFR/Desktop/tushare/TodayData.csv", col_types = cols(code = col_character()))
stocks_cashflow <- read_csv("C:/Users/ShangFR/Desktop/tushare/stocks_cashflow.csv")
stocks_growth <- read_csv("C:/Users/ShangFR/Desktop/tushare/stocks_growth.csv")
stocks_operation <- read_csv("C:/Users/ShangFR/Desktop/tushare/stocks_operation.csv")
stocks_report <- read_csv("C:/Users/ShangFR/Desktop/tushare/stocks_report.csv")
stocks_debtpaying <- read_csv("C:/Users/ShangFR/Desktop/tushare/stocks_debtpaying.csv")

stocks = left_join(stocks_profit[,c(1,2,3)],stocks_basics[,c(1,3,5,15)],by="code")
Q_pe = quantile(stocks$pe,na.rm=TRUE)[-1]
Q_pb = quantile(stocks$pb,na.rm=TRUE)[-1]
Q_roe = quantile(stocks$roe,na.rm=TRUE)[-1]

IQR_pe = Q_pe[3]-Q_pe[1]
MAX_pe = Q_pe[3]+1.5*IQR_pe
IQR_pb = Q_pb[3]-Q_pb[1]
MAX_pb = Q_pb[3]+1.5*IQR_pb
IQR_roe = Q_roe[3]-Q_roe[1]
MAX_roe = Q_roe[3]+1.5*IQR_roe

industry_data =  filter(select(stocks,"pe","pb","roe","industry"),pe>0 & pe<=MAX_pe & pb>0 & pb<=MAX_pb& roe>0 & roe<=MAX_roe) %>%
  group_by(industry) %>%
  summarise(PE = mean(pe),Q_pe = quantile(pe,0.5),dif_pe = PE-Q_pe,
            PB = mean(pb),Q_pb = quantile(pb,0.5),dif_pb = PB-Q_pb,
            ROE = mean(roe),Q_roe = quantile(roe,0.5),dif_roe = ROE-Q_roe)


Today_stocks = left_join(TodayData,stocks_basics[,c(1,3)],by="code")
filter(select(Today_stocks,"changepercent","industry")) %>%
  group_by(industry) %>%
  summarise(PER = mean(changepercent)) %>%
  arrange( desc(PER))


recommend = stocks[sample(1:1000,6),1:2]
basics= as.matrix(filter(stocks_basics,code %in% recommend$code))
library(RJSONIO)
writeLines(toJSON(basics), "C:/Users/ShangFR/Desktop/tushare/basics.json")


codes = unique(recommend$code)
l =length(codes)
result_list<-list()
for(i in 1:l){
  info_list=list()
  info_list$profit= filter(stocks_profit,code %in% codes[i])
  info_list$cashflow= filter(stocks_cashflow,code %in% codes[i])
  info_list$growth= filter(stocks_growth,code %in% codes[i])
  info_list$operation=  filter(stocks_operation ,code %in% codes[i])
  info_list$report= filter(stocks_report,code %in% codes[i])
  info_list$debtpaying= filter(stocks_debtpaying,code %in% codes[i])
  a=info_list$profit[["roe"]]*info_list$profit[["gross_profit_rate"]]
  b=info_list$cashflow[["cf_sales"]]
  info_list$level= c(a,b,200,300,200,100)
  result_list[[i]]=info_list
}
names(result_list)=codes
library(RJSONIO)

writeLines(toJSON(result_list), "C:/Users/ShangFR/Desktop/tushare/info.json")




plot(industry_data$PE,industry_data$PB)
norm.data = scale(industry_data[,c(2,5,8)])
# k取2到8，评估K
K <- 2:8
round <- 3# 每次迭代30次，避免局部最优
rst <- sapply(K,function(i){
  print(paste("K=",i))
  mean(sapply(1:round,function(r){
    print(paste("Round",r))
    result <- kmeans(norm.data, i)
    stats <- cluster.stats(dist(norm.data), result$cluster)
    stats$avg.silwidth
  }))
})
plot(K,rst,type='l',main='轮廓系数与K的关系', ylab='轮廓系数')

# 降纬度观察
k = 2# 根据上面的评估 k=2最优
clu <- kmeans(norm.data,k)
mds = cmdscale(dist(norm.data,method="euclidean"))
plot(mds, col=clu$cluster, main='kmeans聚类 k=2', pch = 19)








mean(stocks_data$pe)
quantile(stocks_data$pe,0.5)
mean(stocks_data$pb)
quantile(stocks_data$pb,0.5)
plot(stocks_data$pe,stocks_data$pb)

#将第一个指标划分为3类
res1<-kmeans(stocks_basics$pe,10)
barplot(table(res1$cluster))
plot(stocks_basics$pe,stocks_basics$pe, col=res1$cluster, main='kmeans聚类 k=2', pch = 19)
plot(stocks_basics$pe,res1$cluster)
#将第二个指标划分为3类
res2<-kmeans(stocks_basics$pb,10)
barplot(table(res2$cluster))
#将聚类结果按列合并在数据集中
res3<-cbind(stocks_basics,res1$cluster,res2$cluster)
Q = quantile(norm.data$pe)
Qb = quantile(norm.data$pb)
norm.data =  filter(select(stocks_basics,"pe","pb","rev"),pe<=Q[4] & pe>0 & pb<=Qb[4] & pb>0)
plot(norm.data$pe,norm.data$pb)
# k取2到8，评估K
K <- 2:3
round <- 3# 每次迭代30次，避免局部最优
rst <- sapply(K,function(i){
  print(paste("K=",i))
  mean(sapply(1:round,function(r){
    print(paste("Round",r))
    result <- kmeans(norm.data, i)
    stats <- cluster.stats(dist(norm.data), result$cluster)
    stats$avg.silwidth
  }))
})
plot(K,rst,type='l',main='轮廓系数与K的关系', ylab='轮廓系数')

# 降纬度观察
old.par <- par(mfrow = c(1,2))
k = 2# 根据上面的评估 k=2最优
clu <- kmeans(norm.data,k)
mds = cmdscale(dist(norm.data,method="euclidean"))
plot(mds, col=clu$cluster, main='kmeans聚类 k=2', pch = 19)
plot(mds, col=iris$Species, main='原始聚类', pch = 19)
par(old.par)




#首先加载软件包
library(fpc)
#利用著名的iris数据集
data=iris[,1:4]
#设簇个数在2到5之间取值
x=c()
y=c()
for (i in 2:5){
  #K聚类结果存于result变量
  result <- kmeans(data,i)
  #求出聚类评价统计量
  stats=cluster.stats(dist(data), result$cluster)
  #将结果存入X
  x[i-1]=stats$avg.silwidth
  y[i-1]=i
}
plot(y,x)

plot(stocks_basics$pe,res1$cluster)



area_industry = select(stocks_basics ,c("industry","area"))
area_industry$num = 1
area_industry = area_industry %>%
  group_by(area,industry) %>%
  summarise(num = sum(num))

area_industry %>% 
  ggplot(aes(x=area,y=num))+geom_bar(stat = "identity",aes(fill = industry))+
  labs(title = "   ",x = "行业分布",y = "上市公司总数")+
  coord_flip()

boxplot(stocks_basics[,5])
log(scale(stocks_basics[,-c(1:4,16)])) 

stocks_basics[,-c(1,2,4,16)]%>%
  group_by(industry) %>%
  quantile()


Pe_MA =  stocks_basics %>%
  group_by(industry,area) %>%
  summarise(pe_MA = mean(pb)) %>%
  arrange(desc(pe_MA))

Pe_MA %>% 
  ggplot(aes(x=area,y=pe_MA))+geom_bar(stat = "identity",aes(fill = industry))+
  labs(title = "   ",x = "行业",y = "pe")+
  coord_flip()


PE = log(stocks_basics$pe)
PE1 = PE
Q = quantile(PE)[-1]
IQR = Q[3]-Q[1]
MAX = Q[3]+1.5*IQR
MIN = Q[1]-1.5*IQR
PE1[PE>=MAX]=3
PE1[PE<MAX & PE>=Q[3]]=6
PE1[PE<Q[3] & PE>=Q[2]]=5
PE1[PE<Q[2] & PE>=Q[1]]=2
PE1[PE<Q[1] & PE>=MIN]=4
PE1[PE<MIN]=1


library(fpc)# install.packages("fpc")
data(iris)
head(iris)
# 0-1 正规化数据
min.max.norm <-function(x){
  (x-min(x))/(max(x)-min(x))
}
raw.data <- iris[,1:4]
norm.data <- data.frame(sl = min.max.norm(raw.data[,1]),
                        sw = min.max.norm(raw.data[,2]),
                        pl = min.max.norm(raw.data[,3]),
                        pw = min.max.norm(raw.data[,4]))



