import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
import numpy as np

def highlight_diff(row):
    if row['Item_x'] != row['Item_y']:
        color = 'red'
    
    background = ['background-color: {}'.format(color) for _ in row]

    return background

    


BoMNAME1 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\THT-MPG3BPJU-03.xlsx').iloc[0,0]
#print(BoMNAME1)
BoMNAME2 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\THT-MPG3BPJU-04.xlsx').iloc[0,0]
#print(BoMNAME2)
df1 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\THT-MPG3BPJU-03.xlsx', usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(how='all').reset_index(drop=True)
#new_row = pd.DataFrame({'Level':'Nan', 'Item':BoMNAME, 'Description':'Nan', 'Ref Designator':'Nan'}, index = [0])

df2 = df1.sort_values(by=['Level','Ref Designator']).reset_index(drop=True)
#print(df2)


df3 = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\THT-MPG3BPJU-04.xlsx', usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(how='all').reset_index(drop=True)
df4 = df3.sort_values(by=['Level','Ref Designator']).reset_index(drop=True)
#print(df4)

bommerge = df2.merge(df4, on=['Level', 'Ref Designator'], how='outer').replace(np.nan, None)
bommerge['New'] = np.where(bommerge['Item_x'] != bommerge['Item_y'], 'Attention!', '')
print(bommerge)
bommerge.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\Result.xlsx')
'''
diff = bommerge['Item_x'].compare(bommerge['Item_y'])
print(diff)
listindex = range(len(diff.index))
for i in range(len(diff.index)):
    diffbom = pd.DataFrame([])
    diffbom = pd.concat([diffbom, bommerge.loc[diff.index[i]]])

print(diffbom)
'''
#print(bommerge)
#bomjoin = df2.set_index(['Level', 'Ref Designator']).join(df4.set_index(['Level', 'Ref Designator']), how='inner', lsuffix=BoMNAME1, rsuffix=BoMNAME2)
#print(bomjoin)
'''
levelzero1 = df2[df2['Level']==str(0)]
#print(levelzero1)
levelzero2 = df4[df4['Level']==str(0)]
#print(levelzero2)
#print(levelList2)
levelZeroDiff = levelzero1.set_index('Ref Designator').join(levelzero2.set_index('Ref Designator'), lsuffix=BoMNAME1, rsuffix=BoMNAME2)
print(levelZeroDiff)

levelone1 = df2[df2['Level']==str(1)]
#print(levelone1)
levelone2 = df4[df4['Level']==str(1)]
#print(levelone2)
#levelonediff = datacompy.Compare(levelone1,levelone2, join_columns=['Level', 'Item', 'Description', 'Ref Designator'], df1_name=BoMNAME1, df2_name=BoMNAME2)
#levelonediff.matches(ignore_extra_columns=False)
#print(levelonediff.df1_unq_rows)
#print(levelonediff.df2_unq_rows)

#levelOneDiff = levelone1.compare(levelone2, keep_shape=True, keep_equal=True, result_names=(BoMNAME1,BoMNAME2))
levelonecompare = levelone1.set_index('Ref Designator').join(levelone2.set_index('Ref Designator'), lsuffix=BoMNAME1,rsuffix=BoMNAME2)
print(levelonecompare)
#levelZeroDiff.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\Result.xlsx')
'''

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
    model = pandasModel(bommerge)
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())
