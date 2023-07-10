import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#create questions
acdcNodes = ['config.version', 'charger.ACCable.show', 'charger.ACPlugMaxVoltage',
             'settings.acvoltagethreshold', 'charger.DCPlug.show', 'cable.name',
             'cable.length', 'apc.autobypass']
acdcDescrip = ["Configuration file Part Number.",
            "AC input cable dropdown will be shown on the configuration page? (True/False)",
            "Maximum AC voltage. (250 for IEC connector or 277 for terminal block)",
            "AC voltage threshold. (90 for G3 single phase)",
            "DC output connector dropdown will be shown on the configuration page? (True/False)",
            "Name of DC output cable size. (1/0AWG for US or 50mm\u00b2 for non-US)",
            "Length of DC output cable. (2.44 for US or 3 for non-US)",
            "Allow use of BMID bypass configuration without user intervention. (True/False)"]
fpNodes = ['display.showchargerrestart', 'timeofday.allowoverride', 'display.outputtest', 'startdelay.allowoverride',
           'equalise.allowoverride']
fpDescrip = ["Allows user to restart the charger's controller using the front panel interface.",
                   "Allows user to override a scheduled off period using the front panel interface.",
                   "Allows user to test the IO expansion board outputs using the front panel interfac",
                   "Allows user to override a start delay",
                   "Allows the user to manually initiate an equalise using the front panel interface."]

class tooltip(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #add status bar to the main window
        self.statusBar().showMessage("Ready")
        #create central widget to the main window
        centWidget = QWidget()
        self.setCentralWidget(centWidget)
        
        #set tooltip font
        QToolTip.setFont(QFont('SansSerif', 10))
        #set label font
        QLabel.setFont(self, QFont('SansSerif',13))
        #create menu bar selection EXIT
        exitAct = QAction('&Exit',self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit Application')
        exitAct.triggered.connect(qApp.quit)
        #create menu bar and add selection then link it with action
        menuBar = self.menuBar()
        exitMenu = menuBar.addMenu('&Exit')
        exitMenu.addAction(exitAct)
        #create grid layout to manage widgets in central widget
        grid = QGridLayout()
        grid.setSpacing(30)
        centWidget.setLayout(grid)
        #create labels within central widget
        for i in range(8):
            lab_Undefinde = QLabel(acdcNodes[i], centWidget)
            lab_Undefinde.setToolTip(acdcDescrip[i])
            lab_Undefinde.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            #lab_Undefinde.resize(lab_Undefinde.sizeHint())
            #lab_Undefinde.move(10,(i*50+50))
            grid.addWidget(lab_Undefinde,i,0,1,5)
        #create buttons within central widget
        btn_Next = QPushButton('Next', centWidget)
        btn_Exit = QPushButton('Exit', centWidget)
        btn_Exit.clicked.connect(qApp.quit)
        btn_Next.resize(btn_Next.sizeHint())
        btn_Exit.resize(btn_Exit.sizeHint())
        btnRow = grid.rowCount() + 1
        grid.addWidget(btn_Exit, btnRow, grid.columnCount()+1)
        grid.addWidget(btn_Next, btnRow, grid.columnCount()+1)
        
        '''#use BoxLayout to manage buttons
        hBox = QHBoxLayout()
        hBox.addStretch(1)
        hBox.addWidget(btn_Exit)
        hBox.addWidget(btn_Next)

        vBox = QVBoxLayout()
        vBox.addStretch(1)
        vBox.addLayout(hBox)

        centWidget.setLayout(vBox)'''
        #specify main window size, position, title
        self.resize(1000,600)
        self.setWindowTitle('ACDCsettings')
        self.center()
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)
    ex = tooltip()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
