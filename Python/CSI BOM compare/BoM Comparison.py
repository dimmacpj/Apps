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
        bomBox1 = QVBoxLayout()
        #bomBox1.addStretch(2)
        bom1Label = QLabel('Open the excel file of the first Indented Current BoM')
        bomBox1.addWidget(bom1Label)
        hBox1 = QHBoxLayout()
        self.bom1Path = QLineEdit()
        self.bom1Path.setFixedSize(600,25)
        hBox1.addWidget(self.bom1Path)
        hBox1.addStretch()
        bom1Button = QPushButton('Open')
        bom1Button.clicked.connect(self.openFile1)
        hBox1.addWidget(bom1Button)
        bomBox1.addLayout(hBox1)
        
#Second BoM excel path
        bomBox2 = QVBoxLayout()
        #bomBox2.addStretch(2)
        bom2Label = QLabel('Open the excel file of the second Indented Current BoM')
       
        bomBox2.addWidget(bom2Label)
        hBox2 = QHBoxLayout()
        self.bom2Path = QLineEdit()
        self.bom2Path.setFixedSize(600,25)
        hBox2.addWidget(self.bom2Path)
        hBox2.addStretch()
        bom2Button = QPushButton('Open')
        bom2Button.clicked.connect(self.openFile2)
        hBox2.addWidget(bom2Button)
        bomBox2.addLayout(hBox2)
        
#Compare result table
        self.resultTable = QtWidgets.QTableView()     
        #self.resultTable.horizontalHeader().setStretchLastSection(True)
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
        self.resize(800, 500)
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
        path1 = self.bom1Path.text()
        path2 = self.bom2Path.text()
        BOMOne = pd.read_excel(path1, usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(
                       how='all').reset_index(drop=True)
        BOMTwo = pd.read_excel(path2, usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(
                       how='all').reset_index(drop=True)
        LengthOne = len(BOMOne)
        LengthTwo = len(BOMTwo)
        BoM1Name = Path(path1).stem
        BoM2Name = Path(path2).stem
        BOMOne.index = [BoM1Name]*LengthOne
        BOMTwo.index = [BoM2Name]*LengthTwo
        self.Result = pd.concat([BOMOne,BOMTwo]).drop_duplicates(keep=False).sort_values('Ref Designator')
        self.model = TableModel(self.Result)
        self.resultTable.setModel(self.model)
        

#function to open excel file
    def openFile1(self):
        excelFile1, unUse1 = QFileDialog.getOpenFileName(self, 'Select a File', r'C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\','Excel (*.xlsx)')
        if excelFile1:
            path1 = Path(excelFile1)
            self.bom1Path.setText(str(path1))
    def openFile2(self):
        excelFile2, unUse2 = QFileDialog.getOpenFileName(self, 'Select a File', r'C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\','Excel (*.xlsx)')
        if excelFile2:
            path2 = Path(excelFile2)
            self.bom2Path.setText(str(path2))     

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
