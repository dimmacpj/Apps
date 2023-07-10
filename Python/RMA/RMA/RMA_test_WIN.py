from os import sep
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

currentYear = 2021
currentMonth = 6

AllLines = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Pandas\\RMA\\RMA\\Lines_June.xlsx', usecols=[
    'RMA', 'Name', 'RMA Date', 'RMA Line', 'Item', 'Description', 'Qty To Return', 'RMA Line Status',
    'Return', 'Warranty', 'Last Return', 'Reason', 'Wty Confirmed', 'EnatelWarrantyVoidReasonGridCol Wty Void Reason',
    'Serial Number', 'Tech Date', 'Root Cause', 'Disposition'])

#print(AllLines['RMA Date'].dt.year)
AllLines = AllLines.loc[(AllLines['RMA'] != 'RMA0200110') & 
                        (AllLines['RMA'] != 'RMA0200111') & 
                        (AllLines['RMA'] != 'RMA0000096')]
AllLines = AllLines.loc[(AllLines['Tech Date'].dt.year == currentYear) & (AllLines['Tech Date'].dt.month == currentMonth)]
ForCrown = AllLines.loc[(AllLines['Name'] == 'Crown Equipment Limited') | 
                        (AllLines['Name'] == 'Crown Equipment Corporation - New Bremen') | 
                        (AllLines['Name'] == 'Crown Equipment Corporation') | 
                        (AllLines['Name'] == 'Crown Equipment Limited')]
ForOther = AllLines.loc[(AllLines['Name'] != 'Crown Equipment Limited') & 
                        (AllLines['Name'] != 'Crown Equipment Corporation - New Bremen') & 
                        (AllLines['Name'] != 'Crown Equipment Corporation') & 
                        (AllLines['Name'] != 'Crown Equipment Limited')]
#AllLines = AllLines.drop_duplicates(['RMA'], ignore_index=True)

#AllLines.to_excel('C:\\Users\\neal.peng\\Documents\\Pandas\\RMA\\RMA\\AllLines.xlsx')
#ForCrown.to_excel('C:\\Users\\neal.peng\\Documents\\Pandas\\RMA\\RMA\\Crown.xlsx')
#ForOther.to_excel('C:\\Users\\neal.peng\\Documents\\Pandas\\RMA\\RMA\\Other.xlsx')

#ServicedOthers = pd.DataFrame()
#WarrantyOthers = pd.DataFrame()
#WarrantyCrown = pd.DataFrame()

#SerCindex = ForCrown.drop_duplicates(['RMA'])
ServicedCrown = pd.DataFrame({'RMA No': ForCrown['RMA'].value_counts().index, 
                              'Qty of investigated': ForCrown['RMA'].value_counts().values,
                              'Qty of repaired': 0,
                              'Qty of BER': 0},
                             index= range(len(ForCrown['RMA'].value_counts().values)))
print(ServicedCrown)

#print(ServicedCrown)
#print(ForCrown)
ForCrown = ForCrown.astype({'Disposition': str})
Repaired = ForCrown[ForCrown['Disposition'].str.contains('Invoice')]
#print(Repaired)
RepairedCount = pd.DataFrame({'RMA No': Repaired['RMA'].value_counts().index,
                              'Qty': Repaired['RMA'].value_counts().values},
                             index= range(len(Repaired['RMA'].value_counts().values)))
print(RepairedCount)
Delt = len(ServicedCrown) - len(RepairedCount)
for i in range(Delt):
    RepairedCount = RepairedCount.append(pd.DataFrame({'RMA No': 'RMA1', 'Qty': 0}, index=[0]))
print(RepairedCount)
ServicedCrown['Qty of investigated'] = RepairedCount[RepairedCount['RMA No'].isin(ServicedCrown['RMA No'])]['Qty'].values
print(ServicedCrown)
'''
Opened = pd.DataFrame()

IndexQty = AllLines.index

OpenedList = list()

for i in IndexQty:
    if AllLines['RMA Line Status'][i] == 'Opened':
        OpenedList.append(i)
Opened = AllLines.iloc[OpenedList]
Opened = Opened.reset_index().drop(['index'], axis=1)

IndexQty = Opened.index
OpenedNoreturnList = list()
for k in IndexQty:
    if Opened['Return'][k] == 1:
        OpenedNoreturnList.append(k)
OpenedNoreturn = pd.DataFrame()
OpenedNoreturn = Opened.iloc[OpenedNoreturnList]
OpenedNoreturn = OpenedNoreturn.reset_index().drop(['index'], axis=1)

IndexQty = OpenedNoreturn.index
NotReceivedList = list()
for l in IndexQty:
    if str(OpenedNoreturn['Root Cause'][l]) == 'nan':
        NotReceivedList.append(l)
NotReceived = pd.DataFrame()
NotReceived = OpenedNoreturn.iloc[NotReceivedList]
NotReceived = NotReceived.reset_index().drop(['index'], axis=1)
print(NotReceived)
'''


'''
RMA = pd.read_excel('C:\\Users\\NUC\\Documents\\Pandas\\RMA.xlsx', usecols=[
    'RMA', 'RMA Date', 'Status', 'Customer'], dtype={'RMA Date':object})
'''

'''
RMA.to_excel('C:\\Users\\NUC\\Documents\\Pandas\\RMA_Report.xlsx')
LineItem.to_excel('C:\\Users\\NUC\\Documents\\Pandas\\LineItem_Report.xlsx')
'''
#print(RMA)
#print(RMA['RMA Date'].dtype)

'''
if RMA['RMA Date'][221].month == 6:  如果index为221的行的月份是六月，则将这一行赋予到一个新的dataframe中 并展示出来，否则显示 false
    new_RMA = RMA.loc[[221]]
    print(new_RMA)
else: print('False')
'''

'''
new_RMA = pd.DataFrame()    #创建一个新的dataframe new_RMA
#   读取RMA中的数据，并将2021年6月的数据添加到型创建的new_RMA中
for i in RMA.index:
    if RMA['RMA Date'][i].year == currentYear:
        if RMA['RMA Date'][i].month == currentMonth:
            new_RMA = new_RMA.append(RMA.loc[[i]], ignore_index=True)
print(new_RMA)
'''

#for i in RMA.index:      
#    print(RMA['RMA Date'][i])        #展示所有日期 相当于print(RMA['RMA Date'])

#for i in RMA.index:      
#    print(RMA['RMA Date'][i].year)      #展示RMA Date 序列中的月份

#new_RMA = RMA[['RMA', 'RMA Date', 'Customer']].set_index([
#    'RMA', 'RMA Date']).sort_values('Customer', ascending=False) #生成新的RMA数据框架 
#并将RMA和RMA Date设置为索引
#print(new_RMA)




'''
RMA_Cust = RMA['Customer']  #提取客户列表
print(RMA_Cust)
Customer_Qty = RMA_Cust.count()  #得到客户列中 非缺失值个数
print(Customer_Qty)
unique_Cust_Array = RMA_Cust.unique()   #得到客户列唯一值组成的列表
print(unique_Cust_Array)
unique_Cust_Qty = RMA_Cust.value_counts()  #得到客户列中唯一值和其对应的频率
print(unique_Cust_Qty)
'''

'''
RMA_Date = RMA['RMA Date']     #提取RMA日期列
print(RMA_Date)
unique_RMA_Date_Array = RMA_Date.unique()    #得到RMA日期列唯一值组成的列表
print(unique_RMA_Date_Array)
'''