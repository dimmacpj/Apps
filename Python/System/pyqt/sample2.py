import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView, QHeaderView, QMainWindow,QTableWidget,QTableWidgetItem
from PyQt5.QtCore import QAbstractTableModel, Qt
import numpy as np
from PyQt5.QtGui import *

BoMNAME1 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\RW624-21.xlsx').iloc[0,0]
#print(BoMNAME1)
BoMNAME2 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\RW624-22.xlsx').iloc[0,0]
#print(BoMNAME2)
df1 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\RW624-21.xlsx', usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(how='all').reset_index(drop=True)
df2 = df1.sort_values(by=['Level','Ref Designator','Item']).replace(np.nan, 'Missing Info').reset_index(drop=True)
df3 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\RW624-22.xlsx', usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(how='all').reset_index(drop=True)
df4 = df3.sort_values(by=['Level','Ref Designator','Item']).replace(np.nan, 'Missing Info').reset_index(drop=True)

df2Desi = df2[df2['Ref Designator']!='Missing Info']
#print(df2Desi)
df2Nodesi = df2[df2['Ref Designator']=='Missing Info'].reset_index(drop=True)
#print(df2Nodesi)
df4Desi = df4[df4['Ref Designator']!='Missing Info']
#print(df4Desi)
df4Nodesi = df4[df4['Ref Designator']=='Missing Info'].reset_index(drop=True)
#print(df4Nodesi['Item'])
#df2Desi.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\df2.xlsx')
#df4Desi.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\df4.xlsx')
nodesiuniq1 = df2Nodesi[~df2Nodesi['Item'].isin(df4Nodesi['Item'])]
#for i in range(len(df2Nodesi)):
    #if df2Nodesi.iloc[i,1] in df4Nodesi['Item'].values.tolist():
        #nodesiuniq1 = nodesiuniq1.drop(i)
nodesiuniq2 = df4Nodesi[~df4Nodesi['Item'].isin(df2Nodesi['Item'])]
#print(df2Nodesi)
#for i in range(len(df4Nodesi)):
    #if df4Nodesi.iloc[i,1] in df2Nodesi['Item'].values.tolist():
        #nodesiuniq2 = nodesiuniq2.drop(i)
#print(df4Nodesi)
bommerge = df2Desi.merge(df4Desi, on=['Level','Ref Designator'], how='outer',suffixes=('_'+BoMNAME1,'_'+BoMNAME2)).replace(np.nan, 'Not in BoM').sort_values(by=['Level','Ref Designator'])
#bommerge.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\bommerge.xlsx')
bommergeuniq = bommerge.copy()
bommergeuniq = bommergeuniq[bommergeuniq['Item_'+BoMNAME1] != bommergeuniq['Item_'+BoMNAME2]]
#bommergeuniq = bommergeuniq[~bommergeuniq['Item_'+BoMNAME1].isin(bommergeuniq['Item_'+BoMNAME2])]
refdesList = bommergeuniq['Ref Designator'].unique().tolist()
print(bommergeuniq)
print(refdesList)
bommergeuniqNew = pd.DataFrame(columns=bommergeuniq.columns)
for refdes in refdesList:
    subdf = bommergeuniq.loc[bommergeuniq['Ref Designator'] == refdes]
    subdf = subdf[~subdf['Item_'+BoMNAME1].isin(subdf['Item_'+BoMNAME2])]
    bommergeuniqNew = pd.concat([bommergeuniqNew, subdf])
    print(bommergeuniqNew)

#print(Desimerge)

Nodesimerge = pd.concat([nodesiuniq1.rename({'Item':'Item_'+BoMNAME1,'Description':'Description_'+BoMNAME1},axis=1),nodesiuniq2.rename({'Level':'Level2','Item':'Item_'+BoMNAME2,'Description':'Description_'+BoMNAME2,'Ref Designator':'Ref2'},axis=1)],axis=1).reset_index(drop=True)
Nodesimerge['Level'] = Nodesimerge['Level'].replace(np.nan,'0').str.replace(r'\D+','').astype(int) + Nodesimerge['Level2'].replace(np.nan,'0').str.replace(r'\D+','').astype(int)
Nodesimerge = Nodesimerge.drop(columns=['Level2','Ref2'])
Nodesimerge['Ref Designator'] = Nodesimerge['Ref Designator'].replace(np.nan,'Missing Info')
Nodesimerge['Item_'+BoMNAME1] = Nodesimerge['Item_'+BoMNAME1].replace(np.nan,'Not in BoM')
Nodesimerge['Item_'+BoMNAME2] = Nodesimerge['Item_'+BoMNAME2].replace(np.nan,'Not in BoM')
Nodesimerge['Description_'+BoMNAME1] = Nodesimerge['Description_'+BoMNAME1].replace(np.nan,'Not in BoM')
Nodesimerge['Description_'+BoMNAME2] = Nodesimerge['Description_'+BoMNAME2].replace(np.nan,'Not in BoM')
print(Nodesimerge)
bommerge = pd.concat([bommergeuniqNew, Nodesimerge])
bommerge['Level'] = bommerge['Level'].astype(str)
bommerge = bommerge.sort_values(by=['Level']).reset_index(drop=True)

#Nodesimerge.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\Nodesimerge.xlsx')

#bommerge.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\bommerge.xlsx')

#print(bommerge)


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

#    def headerData(self, col, orientation, role):
#        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#            return self._data.columns[col]
#        return None
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    windows = QMainWindow()
    view = QTableWidget()
    windows.setCentralWidget(view)
    view.setRowCount(len(bommerge))
    view.setColumnCount(len(bommerge.columns))
    view.setHorizontalHeaderLabels(bommerge.columns)
    
    for i in range(len(bommerge)):
        for j in range(len(bommerge.columns)):
            item = QTableWidgetItem(str(bommerge.iloc[i,j]))
            view.setItem(i,j,item)
            view.horizontalHeader().setSectionResizeMode(j,QHeaderView.ResizeToContents)
            missingInfo = str(bommerge.iloc[i,j])
            if missingInfo == 'Missing Info':
                ref = QTableWidgetItem(str(bommerge.iloc[i,j]))
                ref.setBackground(QBrush(Qt.yellow))
                view.setItem(i,j,ref)
        bom1PN = str(bommerge.iloc[i,1])

        bom2PN = str(bommerge.iloc[i,4])
 
        if bom1PN == 'Not in BoM':
            ref = QTableWidgetItem(str(bommerge.iloc[i,1]))
            ref.setBackground(QBrush(Qt.red))
            view.setItem(i,1,ref)
        if bom2PN == 'Not in BoM':
            ref = QTableWidgetItem(str(bommerge.iloc[i,4]))
            ref.setBackground(QBrush(Qt.red))
            view.setItem(i,4,ref)     
        #if bom1PN != bom2PN:
        #    ref = QTableWidgetItem(str(bommerge.iloc[i,3]))
        #    ref.setBackground(QBrush(Qt.red))
        #    view.setItem(i,3,ref)
    
    windows.show()
    sys.exit(app.exec_())
'''
    for i in range(len(bommerge)):
        ref2 = str(bommerge.iloc[i,7])
        print(bommerge[bommerge.columns[3]])
        if ref2 not in bommerge[bommerge.columns[3]].values.tolist():
                ref1 = QTableWidgetItem(str(bommerge.iloc[i,7]))
                ref1.setBackground(QBrush(Qt.red))
                view.setItem(i,7,ref1)
        for j in range(len(bommerge)):
            lookuparray = str(bommerge.iloc[j,3])
            if lookuparray == ref2:
                bom2pn = str(bommerge.iloc[i,5])
                bom1pn = str(bommerge.iloc[j,1])
                if bom1pn != bom2pn:
                    ref = QTableWidgetItem(str(bommerge.iloc[i,7]))
                    ref.setBackground(QBrush(Qt.red))
                    view.setItem(i,7,ref)
'''

    


'''    
    model = pandasModel(bommerge)
    view = QTableView()
    view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    font = view.horizontalHeader().font()
    font.setBold(True)
    view.horizontalHeader().setFont(font)
    view.setModel(model)
    for i in range(tablelength):
        value1 = view.model().index(i,1).data()
        value2 = view.model().index(i,4).data()
        if value1 != value2:

            print(view.model().index(i,3).data())
    view.resize(1200, 600)
    view.show()
    sys.exit(app.exec_())
'''