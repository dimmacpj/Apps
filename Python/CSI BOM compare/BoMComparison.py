#To do
#Add save file dialog
#add pop up when save file without data in Result
import sys
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import pandas as pd
import numpy as np

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class mainWin(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initWin()

    def initWin(self):
        self.ResultLength = 0
#create menu bar button
        saveResult = QAction('Save to .xlsx file', self)
        saveResult.setShortcut('Ctrl + S')
        saveResult.triggered.connect(self.saveToXLSX)
#create menu bar and add the button
        menuBar = self.menuBar()
        saveMenu = menuBar.addMenu('&Save Result')
        saveMenu.addAction(saveResult)
#set up main layout
        mainWidget = QWidget(self)
        vBoxMain = QVBoxLayout()
#First BoM excel path
        bomBox1 = self.createBoMPathWidget('Open the excel file of the first Indented Current BoM', 1)
#Second BoM excel path
        bomBox2 = self.createBoMPathWidget('Open the excel file of the second Indented Current BoM', 2)
#Compare result table
        self.resultTable = QTableWidget()
        #self.resultTable = QtWidgets.QTableView()
        self.resultTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.resultTable.horizontalHeader().sectionResizeMode(QHeaderView.Stretch)
        headerFont = self.resultTable.horizontalHeader().font()
        headerFont.setBold(True)
        self.resultTable.horizontalHeader().setFont(headerFont)
        self.resultTable.setWordWrap(True) 
        
#create Compare and Close buttons
        buttonBox = QHBoxLayout()
        buttonBox.addStretch(2)
        closeButton = QPushButton('Close')
        closeButton.clicked.connect(qApp.quit)
        compareButton = QPushButton('Compare')
        compareButton.clicked.connect(self.compareBoMs)
        buttonBox.addWidget(closeButton)
        buttonBox.addWidget(compareButton)        
#add all of above components into main layout
        vBoxMain.addLayout(bomBox1)
        vBoxMain.addLayout(bomBox2)
        vBoxMain.addWidget(self.resultTable)
        #vBoxMain.addStretch(10)
        vBoxMain.addLayout(buttonBox)
        mainWidget.setLayout(vBoxMain)
        self.setCentralWidget(mainWidget)
#set main window size and position
        self.resize(1600, 1000)
        self.setWindowTitle('BoM Compare')
        self.center()
        self.show()
#function to determin screen center point and center the main window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
#function to compare result to xlsx
    def saveToXLSX(self):
        self.Result.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\Result.xlsx')
#function to compare two BoMs
    def compareBoMs(self):
        path1 = self.bomPath1.text()
        path2 = self.bomPath2.text()
        BOMOne = pd.read_excel(path1, usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(
                       how='all').reset_index(drop=True)
        df1 = BOMOne.sort_values(by=['Level', 'Ref Designator']).reset_index(drop=True)
        BOMTwo = pd.read_excel(path2, usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(
                       how='all').reset_index(drop=True)
        df2 = BOMTwo.sort_values(by=['Level', 'Ref Designator']).reset_index(drop=True)
        self.Result = df1.merge(df2, on=['Level', 'Ref Designator'], how='outer').replace(np.nan, None)
        #self.ResultLength = len(self.Result)
        #self.Result['Different Part'] = np.where(self.Result['Item_x'] != self.Result['Item_y'], 'Yes!!!', '')
        #self.model = TableModel(self.Result)
        #self.resultTable.setModel(self.model)
        row = len(self.Result)
        colums = len(self.Result.columns)
        self.resultTable.setRowCount(row)
        self.resultTable.setColumnCount(colums)
        self.resultTable.setHorizontalHeaderLabels(self.Result.columns)
        for i in range(row):
            for j in range(colums):
                item = QTableWidgetItem(str(self.Result.iloc[i,j]))
                self.resultTable.setItem(i,j,item)
            bom1PN = str(self.Result.iloc[i,1])
            bom2PN = str(self.Result.iloc[i,4])
            if bom1PN != bom2PN:
                ref = QTableWidgetItem(str(self.Result.iloc[i,3]))
                ref.setBackground(QBrush(Qt.red))
                self.resultTable.setItem(i,3,ref)

#function to create BoM path widget
    def createBoMPathWidget(self, labelText, order):
        bomBox = QVBoxLayout()
        bomLabel = QLabel(labelText)
        bomBox.addWidget(bomLabel)
        hBox = QHBoxLayout()
        if order == 1:
            self.bomPath1 = QLineEdit()
            self.bomPath1.setFixedSize(1000,25)
            hBox.addWidget(self.bomPath1)
            hBox.addStretch()
            bomButton1 = QPushButton('Open')
            bomButton1.clicked.connect(lambda ch,order=order: self.openFile(order))
            hBox.addWidget(bomButton1)
        elif order == 2:
            self.bomPath2 = QLineEdit()
            self.bomPath2.setFixedSize(1000,25)
            hBox.addWidget(self.bomPath2)
            hBox.addStretch()
            bomButton2 = QPushButton('Open')
            bomButton2.clicked.connect(lambda ch,order=order: self.openFile(order))
            hBox.addWidget(bomButton2)
        bomBox.addLayout(hBox)
        return bomBox
#function to open excel file path
    def openFile(self, buttonNumber):
        excelFile, unUse = QFileDialog.getOpenFileName(self, 'Select a File', r'C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\','Excel (*.xlsx)')
        if excelFile:
            path = Path(excelFile)
            if buttonNumber == 1:
                self.bomPath1.setText(str(path))  
            elif buttonNumber == 2:
                self.bomPath2.setText(str(path))
#function to inform close app
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont('Arial', 9))
    ex = mainWin()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()