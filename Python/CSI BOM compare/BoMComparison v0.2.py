#To do
#Add save file dialog
#add pop up when save file without data in Result
import sys
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import pandas as pd
import numpy as np

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
        self.openFilePath = 'C:\\'
        bomBox1 = self.createBoMPathWidget('Open the excel file of the first Indented Current BoM', 1)
#Second BoM excel path
        bomBox2 = self.createBoMPathWidget('Open the excel file of the second Indented Current BoM', 2)
#Result label, check box and refresh button
        labelAndBoX = QHBoxLayout()
        resultLabel = QLabel('Result')
        self.showAllBoX = QCheckBox('Show all items')
        refreshButton = QPushButton('Refresh')
        refreshButton.clicked.connect(self.compareBoMs)
        labelAndBoX.addWidget(resultLabel)
        labelAndBoX.addStretch(1)
        labelAndBoX.addWidget(self.showAllBoX)
        labelAndBoX.addWidget(refreshButton)
        labelAndBoX.addStretch()
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
        vBoxMain.addLayout(labelAndBoX)
        vBoxMain.addWidget(self.resultTable)
        #vBoxMain.addStretch(10)
        vBoxMain.addLayout(buttonBox)
        mainWidget.setLayout(vBoxMain)
        self.setCentralWidget(mainWidget)
#set main window size and position
        self.resize(1000, 800)
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
        #reset table
        self.resultTable.setRowCount(0)
        #Get BoM path and name
        path1 = self.bomPath1.text()
        BoMNAME1 = pd.read_excel(path1).iloc[0,0]
        path2 = self.bomPath2.text()
        BoMNAME2 = pd.read_excel(path2).iloc[0,0]
        #A well sorted BoM 1
        BOMOne = pd.read_excel(path1, usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(
                       how='all').reset_index(drop=True)
        df1 = BOMOne.sort_values(by=['Level', 'Ref Designator','Item']).replace(np.nan, 'Missing Info').reset_index(drop=True)
        #A well sorted BoM 2
        BOMTwo = pd.read_excel(path2, usecols=['Level','Item', 'Description', 'Ref Designator'],
                   dtype={'Level': str, 'Item': str, 'Description': str, 'Ref Designator': str}).dropna(
                       how='all').reset_index(drop=True)
        df2 = BOMTwo.sort_values(by=['Level', 'Ref Designator','Item']).replace(np.nan, 'Missing Info').reset_index(drop=True)
        #New df contains all parts that has ref designator in BoM 1
        df1Desi = df1[df1['Ref Designator']!='Missing Info']
        #New df contains all parts that doesn't have ref designator in BoM 1
        df1Nodesi = df1[df1['Ref Designator']=='Missing Info'].reset_index(drop=True)
        #New df contains all parts that has ref designator in BoM 2
        df2Desi = df2[df2['Ref Designator']!='Missing Info']
        #New df contains all parts that doesn't have ref designator in BoM 2
        df2Nodesi = df2[df2['Ref Designator']=='Missing Info'].reset_index(drop=True)
        #Merge df1Desi and df2Desi, delete duplicate rows
        desiMerge = df1Desi.merge(df2Desi, on=['Level','Ref Designator'], how='outer',suffixes=('_'+BoMNAME1,'_'+BoMNAME2)).replace(np.nan, 'Not in BoM').sort_values(by=['Level','Ref Designator'])
        
        #check how to show the result, only different parts or all parts
        if self.showAllBoX.checkState() == 2:
            '''
            #To be modified
            refdesList = desiMerge['Ref Designator'].unique().tolist()
            desiMergeNew = pd.DataFrame(columns=desiMerge.columns)
            for refdes in refdesList:
                subdf = desiMerge.loc[desiMerge['Ref Designator'] == refdes]
                subdf = subdf[subdf['Item_'+BoMNAME1]==subdf['Item_'+BoMNAME2]]
                desiMergeNew = pd.concat([desiMergeNew, subdf])
            '''
            #Combine df1Nodesi and df2Nodesi, sort values, reset index, replace values, rename columns
            nodesiMerge = pd.concat([df1Nodesi.rename({'Item':'Item_'+BoMNAME1,'Description':'Description_'+BoMNAME1},axis=1),df2Nodesi.rename({'Level':'Level2','Item':'Item_'+BoMNAME2,'Description':'Description_'+BoMNAME2,'Ref Designator':'Ref2'},axis=1)],axis=1).reset_index(drop=True)
            nodesiMerge['Level'] = nodesiMerge['Level'].replace(np.nan,'0').str.replace(r'\D+','').astype(int) + nodesiMerge['Level2'].replace(np.nan,'0').str.replace(r'\D+','').astype(int)
            nodesiMerge = nodesiMerge.drop(columns=['Level2','Ref2'])
            nodesiMerge['Ref Designator'] = nodesiMerge['Ref Designator'].replace(np.nan,'Missing Info')
            nodesiMerge['Item_'+BoMNAME1] = nodesiMerge['Item_'+BoMNAME1].replace(np.nan,'Not in BoM')
            nodesiMerge['Item_'+BoMNAME2] = nodesiMerge['Item_'+BoMNAME2].replace(np.nan,'Not in BoM')
            nodesiMerge['Description_'+BoMNAME1] = nodesiMerge['Description_'+BoMNAME1].replace(np.nan,'Not in BoM')
            nodesiMerge['Description_'+BoMNAME2] = nodesiMerge['Description_'+BoMNAME2].replace(np.nan,'Not in BoM')
            #Combine desiMergeUniq and nodesiMergeUniq to form the result
            self.Result = pd.concat([desiMerge,nodesiMerge])
            self.Result['Level'] = self.Result['Level'].astype(str)
            self.Result = self.Result.sort_values(by=['Level','Ref Designator','Item_'+BoMNAME1,'Item_'+BoMNAME2]).reset_index(drop=True)
        elif self.showAllBoX.checkState() == 0:
            #Compare df1Nodesi with df2Nodesi, and only keep the unique parts
            nodesiuniq1 = df1Nodesi[~df1Nodesi['Item'].isin(df2Nodesi['Item'])]
            nodesiuniq2 = df2Nodesi[~df2Nodesi['Item'].isin(df1Nodesi['Item'])]
            #Delete the row which has same PN in desiMerge
            desiMergeUniq = desiMerge.copy()
            desiMergeUniq = desiMergeUniq[desiMergeUniq['Item_'+BoMNAME1] != desiMergeUniq['Item_'+BoMNAME2]]
            refdesList = desiMergeUniq['Ref Designator'].unique().tolist()
            desiMergeUniqNew = pd.DataFrame(columns=desiMergeUniq.columns)
            for refdes in refdesList:
                subdf = desiMergeUniq.loc[desiMergeUniq['Ref Designator'] == refdes]
                subdf = subdf[~subdf['Item_'+BoMNAME1].isin(subdf['Item_'+BoMNAME2])]
                desiMergeUniqNew = pd.concat([desiMergeUniqNew, subdf])
            #Combine nodesiuniq1 and nodesiuniq2, sort values, reset index, replace values, rename columns
            nodesiMergeUniq = pd.concat([nodesiuniq1.rename({'Item':'Item_'+BoMNAME1,'Description':'Description_'+BoMNAME1},axis=1),nodesiuniq2.rename({'Level':'Level2','Item':'Item_'+BoMNAME2,'Description':'Description_'+BoMNAME2,'Ref Designator':'Ref2'},axis=1)],axis=1).reset_index(drop=True)
            nodesiMergeUniq['Level'] = nodesiMergeUniq['Level'].replace(np.nan,'0').str.replace(r'\D+','').astype(int) + nodesiMergeUniq['Level2'].replace(np.nan,'0').str.replace(r'\D+','').astype(int)
            nodesiMergeUniq = nodesiMergeUniq.drop(columns=['Level2','Ref2'])
            nodesiMergeUniq['Ref Designator'] = nodesiMergeUniq['Ref Designator'].replace(np.nan,'Missing Info')
            nodesiMergeUniq['Item_'+BoMNAME1] = nodesiMergeUniq['Item_'+BoMNAME1].replace(np.nan,'Not in BoM')
            nodesiMergeUniq['Item_'+BoMNAME2] = nodesiMergeUniq['Item_'+BoMNAME2].replace(np.nan,'Not in BoM')
            nodesiMergeUniq['Description_'+BoMNAME1] = nodesiMergeUniq['Description_'+BoMNAME1].replace(np.nan,'Not in BoM')
            nodesiMergeUniq['Description_'+BoMNAME2] = nodesiMergeUniq['Description_'+BoMNAME2].replace(np.nan,'Not in BoM')
            #Combine desiMergeUniq and nodesiMergeUniq to form the result
            self.Result = pd.concat([desiMergeUniqNew,nodesiMergeUniq])
            self.Result['Level'] = self.Result['Level'].astype(str)
            self.Result = self.Result.sort_values(by=['Level','Ref Designator','Item_'+BoMNAME1,'Item_'+BoMNAME2]).reset_index(drop=True)
        #Delete level 0 which is the very top level item name
        self.Result = self.Result.loc[self.Result['Level'].astype(str) != str(0)]
        #Show PD in table widget
        row = len(self.Result)
        colums = len(self.Result.columns)
        self.resultTable.setRowCount(row)
        self.resultTable.setColumnCount(colums)
        self.resultTable.setHorizontalHeaderLabels(self.Result.columns)
        #Coloring the difference
        for i in range(row):
            for j in range(colums):
                item = QTableWidgetItem(str(self.Result.iloc[i,j]))
                self.resultTable.setItem(i,j,item)
                self.resultTable.horizontalHeader().setSectionResizeMode(j,QHeaderView.ResizeToContents)
                if str(self.Result.iloc[i,j]) == 'Missing Info':
                    ref = QTableWidgetItem(str(self.Result.iloc[i,j]))
                    ref.setBackground(QBrush(Qt.yellow))
                    self.resultTable.setItem(i,j,ref)
            bom1PN = str(self.Result.iloc[i,1])
            bom2PN = str(self.Result.iloc[i,4])
            if bom1PN == 'Not in BoM':
                ref = QTableWidgetItem(str(self.Result.iloc[i,1]))
                ref.setBackground(QBrush(Qt.red))
                self.resultTable.setItem(i,1,ref)
            if bom2PN == 'Not in BoM':
                ref = QTableWidgetItem(str(self.Result.iloc[i,4]))
                ref.setBackground(QBrush(Qt.red))
                self.resultTable.setItem(i,4,ref)
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
            bomButton1.clicked.connect(lambda ch,order=order: self.openFile(order,self.openFilePath))
            hBox.addWidget(bomButton1)
        elif order == 2:
            self.bomPath2 = QLineEdit()
            self.bomPath2.setFixedSize(1000,25)
            hBox.addWidget(self.bomPath2)
            hBox.addStretch()
            bomButton2 = QPushButton('Open')
            bomButton2.clicked.connect(lambda ch,order=order: self.openFile(order,self.openFilePath))
            hBox.addWidget(bomButton2)
        bomBox.addLayout(hBox)
        return bomBox
#function to open excel file path
    def openFile(self, buttonNumber,openPath):
        excelFile, unUse = QFileDialog.getOpenFileName(self, 'Select a File', openPath,'Excel (*.xlsx)')
        if excelFile:
            path = Path(excelFile)
            self.openFilePath = str(Path(excelFile).parent)
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
