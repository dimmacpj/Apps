import sys
from pathlib import Path
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
import numpy as np
import pandas as pd

class mainWin(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initWin()

    def initWin(self):
#set up main layout
        mainWidget = QWidget(self)
        vBoxMain = QVBoxLayout()
#create Compare and Close buttons
        buttonBox = QHBoxLayout()
        buttonBox.addStretch(2)
        closeButton = QPushButton('Close')
        closeButton.clicked.connect(qApp.quit)
        compareButton = QPushButton('Compare')
        compareButton.clicked.connect(self.compareBoMs)
        buttonBox.addWidget(closeButton)
        buttonBox.addWidget(compareButton)
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
        self.resultTable = QTableWidget()
        #self.resultTable.setRowCount(30)
        #self.resultTable.setColumnCount(5)
        #self.resultTable.horizontalHeader().setStretchLastSection(True)
        
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
#function to compare two BoMs
    def compareBoMs(self):
        path1 = self.bom1Path.text()
        path2 = self.bom2Path.text()
        BOMOne = pd.read_excel(path1, usecols=['Item', 'Description', 'Ref Designator'])
        BOMTwo = pd.read_excel(path2, usecols=['Item', 'Description', 'Ref Designator'])
        LengthOne = len(BOMOne)
        LengthTwo = len(BOMTwo)
        BoM1Name = Path(path1).stem
        BoM2Name = Path(path2).stem
        BOMOne.index = [BoM1Name]*LengthOne
        BOMTwo.index = [BoM2Name]*LengthTwo
        Result = pd.concat([BOMOne,BOMTwo]).drop_duplicates(keep=False).sort_values('Ref Designator')
        Result.to_excel('C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\Result.xlsx')

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

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont('Arial', 9))
    ex = mainWin()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

