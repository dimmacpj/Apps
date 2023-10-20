import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt

df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})

df = pd.read_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\THT-MPG3BPJU-04.xlsx', usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(how='all').reset_index(drop=True)
print(df)
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

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())