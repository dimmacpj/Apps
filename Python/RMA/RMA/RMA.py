import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def CountRMArequest():
    #引入全局变量
    global RMAsInYM
    #创建本地变量
    n = 1
    #通过while循环，分别统计各个月份RMA的申请数量，截至到当前月份
    while n <= Month:
        #遍历ForRMAChart中的所有行
        for j in ForRMAChart.index:
            #检查该行RMA创建的年份是否等于当前年份
            if ForRMAChart['RMA Date'][j].year == Year:
                #检查是否等于相应月份
                if ForRMAChart['RMA Date'][j].month == n:
                    #提取整行数据并重置index
                    RMAsInYM = RMAsInYM.append(ForRMAChart.loc[[j]], ignore_index=True)
        #统计RMA的数量并存入到RMARequestCount列表中
        RMARequestCount.append(RMAsInYM['RMA'].count())
        #清空DF中的数据 以免数据叠加
        RMAsInYM.drop([m for m in range(len(RMAsInYM.index))], inplace=True)
        #遍历十二个月，将相应月份的名称存入到MonthsList列表中
        for i in range(1, 13):
            if i == n:
                MonthsList.append(MonthName[i-1])
        n += 1

    return

def CountRMAReceived():
    #本函数与CountRMArequest()仅参数不同，可参考CountRMArequest()的标注
    global RMAsInYM
    n = 1
    
    while n <= Month:

        for j in ForRMAChart.index:
            if ForRMAChart['Last Return'][j].year == Year:
                if ForRMAChart['Last Return'][j].month == n:
                    RMAsInYM = RMAsInYM.append(ForRMAChart.loc[[j]], ignore_index=True)
        RMAReceivedCount.append(RMAsInYM['RMA'].count())
        
        RMAsInYM.drop([m for m in range(len(RMAsInYM.index))], inplace=True)
        
        n += 1

    return

def CountNotReceived():
    #引入全局变量
    global RMAsInYM
    global ForRMAChart
    #创建本地变量
    n = 1
    #创建一个本地DataFrame用以存储最终筛选的数据
    NotReceived = pd.DataFrame()
    #将Root Cause列中的数据格式转换为string，默认是float
    ForRMAChart = ForRMAChart.astype({'Root Cause': str})
    #进行数据筛选并存入本地的DataFrame中
    NotReceived = ForRMAChart.loc[(ForRMAChart['RMA Line Status'] == 'Opened') &
                                  (ForRMAChart['Return'] == 1) &
                                  (ForRMAChart['Root Cause'].isin(['nan']))]
    #重置index
    NotReceived = NotReceived.reset_index().drop(['index'], axis=1) 
    #统计没有收到的RMA数量，并存入到RMANotReceivedCount列表中
    RMANotReceivedCount.append(NotReceived['RMA'].count())
    '''
    while n <= Month:

        for j in NotReceived.index:
            if NotReceived['RMA Date'][j].year == Year:
                if NotReceived['Last Return'][j].month == n:
                    RMAsInYM = RMAsInYM.append(NotReceived.loc[[j]], ignore_index=True)
        
        RMANotReceivedCount.append(NotReceived['RMA'].count())
        #清空DF中的数据 以免数据叠加
        RMAsInYM.drop([m for m in range(len(RMAsInYM.index))], inplace=True)
        
        n += 1
    '''
    return

def CountCrownRMARepaired():
    global ForItemChartCrown
    #将此DF的disposition列转换为string类型
    #ForItemChartCrown = ForItemChartCrown.astype({'Disposition': str})
    #新建DF用于提取所有修复产品的数据
    RepairedCrown = ForItemChartCrown[ForItemChartCrown['Disposition'].str.contains('Invoice|Serviced|Return')]
    #print(Repaired)
    #新建DF并使用value_counts()来统计各个RMA所修复产品的数量
    RepairedCount = pd.DataFrame({'RMA No': RepairedCrown['RMA'].value_counts().index,
                                'Qty of repaired': RepairedCrown['RMA'].value_counts().values},
                                index= range(len(RepairedCrown['RMA'].value_counts().values)))
    #print(RepairedCount)
    #将上面所统计出的修复产品的数量复制到用于绘图的总统计DF中
    for i in ServicedCrownCountForPlot.index:
        for j in RepairedCount.index:
            if ServicedCrownCountForPlot.iloc[i,0] == RepairedCount.iloc[j,0]:
                ServicedCrownCountForPlot.iloc[i,2] = RepairedCount.iloc[j,1]
    return

def CountCrownBER():
    global ForItemChartCrown
    BERCrown = pd.DataFrame()
    #将此DF的disposition列转换为string类型
    #ForItemChartCrown = ForItemChartCrown.astype({'Disposition': str})
    #新建DF用于提取所有修复产品的数据
    BERCrown = ForItemChartCrown[ForItemChartCrown['Disposition'].str.contains('BER|12|Investigation')]
    #print(Repaired)
    #新建DF并使用value_counts()来统计各个RMA所修复产品的数量
    BERCount = pd.DataFrame({'RMA No': BERCrown['RMA'].value_counts().index,
                                'Qty of BER': BERCrown['RMA'].value_counts().values},
                                index= range(len(BERCrown['RMA'].value_counts().values)))
    #print(BERCount)
    #将上面所统计出的修复产品的数量复制到用于绘图的总统计DF中
    for i in ServicedCrownCountForPlot.index:
        for j in BERCount.index:
            if ServicedCrownCountForPlot.iloc[i,0] == BERCount.iloc[j,0]:
                ServicedCrownCountForPlot.iloc[i,3] = BERCount.iloc[j,1]
    return

def CountOthersRMARepaired():
    global ForItemChartAllOther
    #将此DF的disposition列转换为string类型
    #ForItemChartAllOther = ForItemChartAllOther.astype({'Disposition': str})
    #新建DF用于提取所有修复产品的数据
    RepairedOther = ForItemChartAllOther[ForItemChartAllOther['Disposition'].str.contains('Invoice|Serviced|Ready|ready')]
    #print(Repaired)
    #新建DF并使用value_counts()来统计各个RMA所修复产品的数量
    RepairedCount = pd.DataFrame({'RMA No': RepairedOther['RMA'].value_counts().index,
                                'Qty of repaired': RepairedOther['RMA'].value_counts().values},
                                index= range(len(RepairedOther['RMA'].value_counts().values)))
    #print(RepairedCount)
    #将上面所统计出的修复产品的数量复制到用于绘图的总统计DF中
    for i in ServicedOthersCountForPlot.index:
        for j in RepairedCount.index:
            if ServicedOthersCountForPlot.iloc[i,0] == RepairedCount.iloc[j,0]:
                ServicedOthersCountForPlot.iloc[i,2] = RepairedCount.iloc[j,1]
    return

def CountOhtersBER():
    global ForItemChartAllOther
    BEROther = pd.DataFrame()
    #将此DF的disposition列转换为string类型
    #ForItemChartAllOther = ForItemChartAllOther.astype({'Disposition': str})
    #新建DF用于提取所有修复产品的数据
    BEROther = ForItemChartAllOther[ForItemChartAllOther['Disposition'].str.contains('BER|Investigation')]
    #print(Repaired)
    #新建DF并使用value_counts()来统计各个RMA所修复产品的数量
    BERCount = pd.DataFrame({'RMA No': BEROther['RMA'].value_counts().index,
                                'Qty of BER': BEROther['RMA'].value_counts().values},
                                index= range(len(BEROther['RMA'].value_counts().values)))
    #print(BERCount)
    #将上面所统计出的修复产品的数量复制到用于绘图的总统计DF中
    for i in ServicedOthersCountForPlot.index:
        for j in BERCount.index:
            if ServicedOthersCountForPlot.iloc[i,0] == BERCount.iloc[j,0]:
                ServicedOthersCountForPlot.iloc[i,3] = BERCount.iloc[j,1]
    return

def CountInWarrOthers():
    global ForItemChartAllOther
    #提取非Crown in warranty 的数据
    InWarrantyOthers = ForItemChartAllOther.loc[(ForItemChartAllOther['Warranty'] == 1)]
    InWarrCount = pd.DataFrame({'RMA No': InWarrantyOthers['RMA'].value_counts().index,
                                'Qty of In Warranty': InWarrantyOthers['RMA'].value_counts().values},
                                index= range(len(InWarrantyOthers['RMA'].value_counts().values)))
    for i in WarrantyOthersCountForPlot.index:
        for j in InWarrCount.index:
            if WarrantyOthersCountForPlot.iloc[i,0] == InWarrCount.iloc[j,0]:
                WarrantyOthersCountForPlot.iloc[i,1] = InWarrCount.iloc[j,1]
    return

def CountOutWarrOthers():
    global ForItemChartAllOther
    #提取非Crown out of warranty 的数据
    OutWarrantyOthers = ForItemChartAllOther.loc[(ForItemChartAllOther['Warranty'] == 0)]
    OutWarrCount = pd.DataFrame({'RMA No': OutWarrantyOthers['RMA'].value_counts().index,
                                 'Qty of Out of Warranty': OutWarrantyOthers['RMA'].value_counts().values},
                                 index= range(len(OutWarrantyOthers['RMA'].value_counts().values)))
    #print(WarrantyOthersCountForPlot)
    #print(OutWarrCount)
    for i in WarrantyOthersCountForPlot.index:
        for j in OutWarrCount.index:
            if WarrantyOthersCountForPlot.iloc[i,0] == OutWarrCount.iloc[j,0]:
                WarrantyOthersCountForPlot.iloc[i,2] = OutWarrCount.iloc[j,1]
    return

def CountVoidOthers():
    global ForItemChartAllOther
    VoidOthers = ForItemChartAllOther.loc[(ForItemChartAllOther['Wty Confirmed'] == 'No')]
    VoidOhters = VoidOthers['EnatelWarrantyVoidReasonGridCol Wty Void Reason'].str.contains('Fault|AC|Adverse|Customer|Not')
    VoidCount = pd.DataFrame({'RMA No': VoidOthers['RMA'].value_counts().index,
                              'Qty of Voided': VoidOthers['RMA'].value_counts().values},
                              index= range(len(VoidOthers['RMA'].value_counts().values)))
    for i in WarrantyOthersCountForPlot.index:
        for j in VoidCount.index:
            if WarrantyOthersCountForPlot.iloc[i,0] == VoidCount.iloc[j,0]:
                WarrantyOthersCountForPlot.iloc[i,3] = VoidCount.iloc[j,1]
    return

def CountInWarrCrown():
    global ForItemChartCrown
    #提取Crown in warranty 的数据
    InWarrantyCrown = ForItemChartCrown.loc[(ForItemChartCrown['Warranty'] == 1)]
    InWarrCount = pd.DataFrame({'RMA No': InWarrantyCrown['RMA'].value_counts().index,
                                'Qty of In Warranty': InWarrantyCrown['RMA'].value_counts().values},
                                index= range(len(InWarrantyCrown['RMA'].value_counts().values)))
    for i in WarrantyCrownCountForPlot.index:
        for j in InWarrCount.index:
            if WarrantyCrownCountForPlot.iloc[i,0] == InWarrCount.iloc[j,0]:
                WarrantyCrownCountForPlot.iloc[i,1] = InWarrCount.iloc[j,1]
    return

def CountOutWarrCrown():
    global ForItemChartCrown
    #提取Crown out of warranty 的数据
    OutWarrantyCrown = ForItemChartCrown.loc[(ForItemChartCrown['Warranty'] == 0)]
    OutWarrCount = pd.DataFrame({'RMA No': OutWarrantyCrown['RMA'].value_counts().index,
                                 'Qty of Out of Warranty': OutWarrantyCrown['RMA'].value_counts().values},
                                 index= range(len(OutWarrantyCrown['RMA'].value_counts().values)))
    #print(WarrantyOthersCountForPlot)
    #print(OutWarrCount)
    for i in WarrantyCrownCountForPlot.index:
        for j in OutWarrCount.index:
            if WarrantyCrownCountForPlot.iloc[i,0] == OutWarrCount.iloc[j,0]:
                WarrantyCrownCountForPlot.iloc[i,2] = OutWarrCount.iloc[j,1]
    return

def CoutnVoidCrown():
    global ForItemChartCrown
    VoidedCrown = ForItemChartCrown.loc[(ForItemChartCrown['Wty Confirmed'] == 'No')]
    VoidedCrown = VoidedCrown.loc[VoidedCrown['EnatelWarrantyVoidReasonGridCol Wty Void Reason'].str.contains('Fault|AC|Adverse|Customer|Not')]
    VoidCount = pd.DataFrame({'RMA No': VoidedCrown['RMA'].value_counts().index,
                              'Qty of Voided': VoidedCrown['RMA'].value_counts().values},
                              index= range(len(VoidedCrown['RMA'].value_counts().values)))
    for i in WarrantyCrownCountForPlot.index:
        for j in VoidCount.index:
            if WarrantyCrownCountForPlot.iloc[i,0] == VoidCount.iloc[j,0]:
                WarrantyCrownCountForPlot.iloc[i,3] = VoidCount.iloc[j,1]
    return
    

#询问‘要查询哪一年的数据’
#Year = input('Which year of data you want? Please type in numbers')     
#询问‘要查询哪一月的数据’
#Month = input('Which month of data you want? Please type in numbers')   

#获取当前年份
Year = datetime.now().year
#Year = 2021
#获取当前月份
Month = 11
#Month = datetime.now().month
#创建一个列表用以存储各个月RMA申请的数量
RMARequestCount = []
#创建一个列表用以存储各个月RMA到件的数量   
RMAReceivedCount = []
#创建一个列表用以存储所有未到件RMA的数量   
RMANotReceivedCount = []
#创建一个列表用以存储截至到当前月份，各个表月的名称，用来作为图标的x轴   
MonthsList = []
#创建一个列表并预存十二个月份的名称   
MonthName = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                         'Sep', 'Oct', 'Nov', 'Dec']
#读取特定列名的所有lineitem数据
AllLines = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Pandas\\RMA\\Lines.xlsx', usecols=[
    'RMA', 'Name', 'RMA Date', 'RMA Line', 'Item', 'Description', 'Qty To Return', 'RMA Line Status',
    'Return', 'Warranty', 'Last Return', 'Reason', 'Wty Confirmed', 'EnatelWarrantyVoidReasonGridCol Wty Void Reason',
    'Serial Number', 'Tech Date', 'Root Cause', 'Disposition'])
#删除不用的RMA RMA200110 RMA200111 RMA96
AllLines = AllLines.loc[(AllLines['RMA'] != 'RMA0200110') & 
                        (AllLines['RMA'] != 'RMA0200111') & 
                        (AllLines['RMA'] != 'RMA0000096')]
#将此DF的void reason and disposition列转换为string类型
AllLines = AllLines.astype({'EnatelWarrantyVoidReasonGridCol Wty Void Reason':str, 'Disposition': str})

#*****以下为RMA申请接收相关代码*****

#提取‘RMA’列的唯一值并重置index
ForRMAChart = AllLines.drop_duplicates(['RMA'], ignore_index=True)
#创建新的DF用以存储所选年份+月份的数据
RMAsInYM = pd.DataFrame()
#提取数据并存储到RMAsInYM中
#统计截至到当前月份，各个月RMA申请的数量，计算的数量存储到RMARequestCount列表中，月份名称提取到MonthList列表中
CountRMArequest()
#统计截至到当前月份，各个月收到RMA的数量，计算的数量存储到RMAReceivedCount列表中，月份名称提取到MonthList列表中
CountRMAReceived()
#统计当前月份还未收到的RMA数量，并存储到RMANotReceivedCount列表中，通常为一个数值
CountNotReceived()

#创建新的dataframe用于导出图表1（包含RMA Request和RMA Received）
RMAsforPlot = pd.DataFrame(data={'RMAs Requested': RMARequestCount, 'RMAs Received': RMAReceivedCount}, 
                           index=MonthsList )
#print(RMAsforPlot)
#创建一个列表用以存储当前月份的名称，作为图表2（仅包含Not Received RMA）的x轴
#由于DataFrame的index在赋值时必须的列表，因此即使仅一个参数也需要存储到列表中
NotReceivedIndex = []
NotReceivedIndex.append(MonthName[Month - 1])
#print(RMANotReceivedCount)
#创建新的dataframe用于导出图表2（仅包含Not Received RMA）
NotbackRMAsPlot = pd.DataFrame(data={'Not Received RMAs': RMANotReceivedCount}, 
                           index=NotReceivedIndex)

#将RMA Request和RMA Received的数据存储到一个Excel文档中
RMAsforPlot.to_excel('C:\\Users\\neal.peng\\Documents\\Pandas\\RMA\\RMAsforPlot.xlsx')
#导出图表1，横轴命名为‘Month’，纵轴命名为‘Count’，文字横向，将两种数据分开表示
RMAsforPlot.plot.bar(xlabel='Month', ylabel='Count', rot=0, subplots=True)
#导出图表2，横轴命名为‘Month’，纵轴命名为‘Count’，文字横向
NotbackRMAsPlot.plot.bar(xlabel='Month', ylabel='Count', rot=0)
#弹出窗口，显示所有图表
plt.show()


#*****以下为LineItem的保修相关代码*****

#提取当前月份的所有处理过的item数据，并存于一个新的DF ForItemChart中
ServicedRMA = AllLines.loc[(AllLines['Tech Date'].dt.year == Year) & 
                           (AllLines['Tech Date'].dt.month == Month)]
#提取非Crown的数据
ForItemChartAllOther = ServicedRMA.loc[(ServicedRMA['Name'] != 'Crown Equipment Limited') & 
                                    (ServicedRMA['Name'] != 'Crown Equipment Corporation - New Bremen') & 
                                    (ServicedRMA['Name'] != 'Crown Equipment Corporation') & 
                                    (ServicedRMA['Name'] != 'Crown Equipment Pty Ltd')]
#提取Crown的数据
ForItemChartCrown = ServicedRMA.loc[(ServicedRMA['Name'] == 'Crown Equipment Limited') | 
                                 (ServicedRMA['Name'] == 'Crown Equipment Corporation - New Bremen') | 
                                 (ServicedRMA['Name'] == 'Crown Equipment Corporation') | 
                                 (ServicedRMA['Name'] == 'Crown Equipment Pty Ltd')]
#新建一个DF将包含RMA号，各个RMA所保修内的产品数量，各个RMA超过保修期的数量，各个RMA 违反保修条款的数量
#利用value_counts()统计各个RMA号出现的次数，返回一个序列
#将所有数量的初始值设置为零
#index为返回序列的长度
WarrantyCrownCountForPlot = pd.DataFrame({'RMA No': ForItemChartCrown['RMA'].value_counts().index, 
                              'Qty of In Warranty': 0,
                              'Qty of Out of Warranty': 0,
                              'Qty of Voided': 0},
                             index= range(len(ForItemChartCrown['RMA'].value_counts().values)))
WarrantyOthersCountForPlot = pd.DataFrame({'RMA No': ForItemChartAllOther['RMA'].value_counts().index, 
                              'Qty of In Warranty': 0,
                              'Qty of Out of Warranty': 0,
                              'Qty of Voided': 0},
                             index= range(len(ForItemChartAllOther['RMA'].value_counts().values)))
CountOutWarrOthers()
CountInWarrOthers()
CountVoidOthers()

CountOutWarrCrown()
CountInWarrCrown()
CoutnVoidCrown()
TotalWarrantyOther = WarrantyOthersCountForPlot.drop('RMA No', axis=1).sum()
TotalWarrantyCrown = WarrantyCrownCountForPlot.drop('RMA No', axis=1).sum()
WarrantyCrownCountForPlot.append(TotalWarrantyCrown, ignore_index=True).to_excel('C:\\Users\\neal.peng\\Documents\\Pandas\\RMA\\WarrantyCrownCountForPlot.xlsx')
WarrantyOthersCountForPlot.append(TotalWarrantyOther, ignore_index=True).to_excel('C:\\Users\\neal.peng\\Documents\\Pandas\\RMA\\WarrantyOthersCountForPlot.xlsx')
#新建一个DF将包含RMA号，各个RMA所处理的产品数量，各个RMA所修复产品的数量，各个RMA BER的数量
#利用value_counts()统计各个RMA号出现的次数，返回一个序列
#并将此设置为各个RMA所处理的产品数量 
#修复产品的数量和BER的数量设置为零
#index为返回序列的长度
ServicedCrownCountForPlot = pd.DataFrame({'RMA No': ForItemChartCrown['RMA'].value_counts().index, 
                              'Qty of investigated': ForItemChartCrown['RMA'].value_counts().values,
                              'Qty of repaired': 0,
                              'Qty of BER': 0},
                             index= range(len(ForItemChartCrown['RMA'].value_counts().values)))
ServicedOthersCountForPlot = pd.DataFrame({'RMA No': ForItemChartAllOther['RMA'].value_counts().index, 
                              'Qty of investigated': ForItemChartAllOther['RMA'].value_counts().values,
                              'Qty of repaired': 0,
                              'Qty of BER': 0},
                             index= range(len(ForItemChartAllOther['RMA'].value_counts().values)))

CountCrownRMARepaired()
CountCrownBER()
CountOthersRMARepaired()
CountOhtersBER()
TotalServicedCrown = ServicedCrownCountForPlot.drop('RMA No', axis=1).sum()
TotalServicedOther = ServicedOthersCountForPlot.drop('RMA No', axis=1).sum()
ServicedCrownCountForPlot.append(TotalServicedCrown, ignore_index=True).to_excel('C:\\Users\\neal.peng\\Documents\\Pandas\\RMA\\ServicedCrownCountForPlot.xlsx')
ServicedOthersCountForPlot.append(TotalServicedOther, ignore_index=True).to_excel('C:\\Users\\neal.peng\\Documents\\Pandas\\RMA\\ServicedOthersCountForPlot.xlsx')

TotalWarrantyCrown.plot.bar(ylabel='Count', rot=0)
plt.show()
TotalWarrantyOther.plot.bar(ylabel='Count', rot=0)
plt.show()
TotalServicedCrown.plot.bar(ylabel='Count', rot=0)
plt.show()
TotalServicedOther.plot.bar(ylabel='Count', rot=0)
plt.show()


