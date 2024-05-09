import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QHeaderView, QMainWindow,QTableWidget,QTableWidgetItem
from PyQt5.QtCore import QAbstractTableModel, Qt
import numpy as np
from PyQt5.QtGui import *

BoMNAME1 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\FLEXI1-BLK001.xlsx').iloc[0,0]
BoMNAME2 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\FLEXI1-BLK002.xlsx').iloc[0,0]
df1 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\FLEXI1-BLK001.xlsx', usecols=['Level','Item', 'Description', 'Qty Per','U/M','Per'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Qty Per': str, 'U/M': str, 'Per': str}).dropna(how='all').reset_index(drop=True)
df2 = df1.replace(np.nan, 'Missing Info').reset_index(drop=True)
df3 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\FLEXI1-BLK002.xlsx', usecols=['Level','Item', 'Description', 'Qty Per','U/M','Per'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Qty Per': str, 'U/M': str, 'Per': str}).dropna(how='all').reset_index(drop=True)
df4 = df3.replace(np.nan, 'Missing Info').reset_index(drop=True)

bom1level1 = df2.loc[df2['Level'] == '1'].reset_index(drop=True)
#print(bom1level1)
bom1level2 = df2.loc[df2['Level'] == '2'].reset_index(drop=True)
#print(bom1level2)
bom2level1 = df4.loc[df4['Level'] == '1'].reset_index(drop=True)
#print(bom2level1)
bom2level2 = df4.loc[df4['Level'] == '2'].reset_index(drop=True)
#print(bom2level2)
bom1l1uniq = bom1level1[~bom1level1['Item'].isin(bom2level1['Item'])]
bom2l1uniq = bom2level1[~bom2level1['Item'].isin(bom1level1['Item'])]
bom1l2uniq = bom1level2[~bom1level2['Item'].isin(bom2level2['Item'])]
bom2l2uniq = bom2level2[~bom2level2['Item'].isin(bom1level2['Item'])]
level1Compare = pd.concat([bom1l1uniq,bom2l1uniq.rename({'Level':'Level2'},axis=1)],axis=1)
level2Compare = pd.concat([bom1l2uniq,bom2l2uniq.rename({'Level':'Level2'},axis=1)],axis=1)
'''
df2Desi = df2[df2['Ref Designator']!='Missing Info']
df2Nodesi = df2[df2['Ref Designator']=='Missing Info'].reset_index(drop=True)
df4Desi = df4[df4['Ref Designator']!='Missing Info']
df4Nodesi = df4[df4['Ref Designator']=='Missing Info'].reset_index(drop=True)
#df2Desi.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\df2.xlsx')
#df4Desi.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\df4.xlsx')
nodesiuniq1 = df2Nodesi[~df2Nodesi['Item'].isin(df4Nodesi['Item'])]
nodesiuniq2 = df4Nodesi[~df4Nodesi['Item'].isin(df2Nodesi['Item'])]
print(nodesiuniq1)
bommerge = df2Desi.merge(df4Desi, on=['Level','Ref Designator'], how='outer',suffixes=('_'+BoMNAME1,'_'+BoMNAME2)).replace(np.nan, 'Not in BoM').sort_values(by=['Level','Ref Designator'])
#bommerge.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\bommerge.xlsx')
bommergeuniq = bommerge.copy()
bommergeuniq = bommergeuniq[bommergeuniq['Item_'+BoMNAME1] != bommergeuniq['Item_'+BoMNAME2]]
refdesList = bommergeuniq['Ref Designator'].unique().tolist()
bommergeuniqNew = pd.DataFrame(columns=bommergeuniq.columns)
for refdes in refdesList:
    subdf = bommergeuniq.loc[bommergeuniq['Ref Designator'] == refdes]
    subdf = subdf[~subdf['Item_'+BoMNAME1].isin(subdf['Item_'+BoMNAME2])]
    bommergeuniqNew = pd.concat([bommergeuniqNew, subdf])
Nodesimerge = pd.concat([nodesiuniq1.rename({'Item':'Item_'+BoMNAME1,'Description':'Description_'+BoMNAME1},axis=1),nodesiuniq2.rename({'Level':'Level2','Item':'Item_'+BoMNAME2,'Description':'Description_'+BoMNAME2,'Ref Designator':'Ref2'},axis=1)],axis=0).reset_index(drop=True)
print(Nodesimerge)
Nodesimerge['Level'] = Nodesimerge['Level'].replace(np.nan,'0').str.replace(r'\D+','').astype(int) + Nodesimerge['Level2'].replace(np.nan,'0').str.replace(r'\D+','').astype(int)
Nodesimerge = Nodesimerge.drop(columns=['Level2','Ref2'])
print(Nodesimerge)
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
'''
print(level1Compare)
print(level2Compare)
bommerge = pd.concat([level1Compare,level2Compare])
#bommerge = bommerge.loc[bommerge['Level'].astype(str) != str(0)]
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
    view.setSortingEnabled(True)
    
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

    
    windows.show()
    sys.exit(app.exec_())
