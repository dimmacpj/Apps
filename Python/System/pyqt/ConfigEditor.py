import sys
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget

#create setting dicts
settingNodes = ['Part Number and Region', 'AC input and DC output cables and connectors', 'Front panel interface', 'Charger labelling',
                'Battery template set', 'Cabinet type', 'Advanced controller', 'Extra entry', 'Add new node']
regionInfo = {'config.version':'Model Specific Configuration File Part Number',
              'time.zone.name': 'Set the time zone',
              'locale.name': 'Set the locale',
              'locale.enabledlocales': 'Set the list of locales that the user can select from'}
acdcInfo = {'charger.ACCable.show':'Determines if the AC input calbe dropdown will be shown on the configuration page',
            'charger.DCPlug.show':'Determins if the DC output connector dropdown will be shown on the configuration page',
            'cable.name':'Name of DC output cable size (1/0AWG for US or 50mm\u00b2 for non-US)',
            'cable.length':'Length of DC output cable (2.44 for US or 3 for non-US)',
            'apc.autobypass':'Allow use of BMID bypass configuration without user intervention. True for US only',
            'settings.acvoltagethreshold':'Sets this as a proportion of the configured AC supply. Only for single phase (90 for G3 single phase)',
            'charger.ACPlugMaxVoltage':'Upper limit on the AC input voltage of a charger. Only for single phase. Determined by connector type (250 for IEC connector or 277 for terminal block)',
            'charger.ACCable':'AC input cable fitted to charger',
            'charger.ACConfigurations':'AC Supply configuration',
            'charger.DCPlug':'DC output connector fitted to detachable output cable',
            'cable.area':'Cross section of DC output cable'}
fpInfo = {'display.showchargerrestart':"Allow user to restart the charger's controller using the front panel interface",
          'timeofday.allowoverride':'Allow user to override a scheduled off period using the front panel interface',
          'display.outputtest':'Allow user to test the IO expansion board output using the front panel interface',
          'startdelay.allowoverride':'Allow user to override a start delay',
          'eualise.allowoverride':'Allow user to manually initiate an equalise using the front panel interface'}
labelInfo = {'charger.ulBatteryType': 'Set what is displayed in the BATTERY TYPE field on the HWC label',
             'charger.ulBatteryTypeOptions': 'Set the battery types a use can select from when printing the HWC label'}
templateInfo = {'charger.templatefiename':'Name of template file on charger',
                'charger.template':'Battery template sets'}
cabinetInfo = {'device.model_type':'G3 model type (Leave it empty for Mainlin product or type in ENT for Entry Level product)',
               'charger.FrameSize':'Cabinet frame size',
               'charger.MaxModuleCount':'Maximum number of modules a charger can accommodate',
               'charger.FixedModuleConfiguration':'Set a fixed module type and count for the charger (For G3 three phase Entry Level and all single phase)',
               'modules.maximumcurrent':'Maximum output current for each module (Set for G3 single phase only)',
               'charger.dualconnector.enable':'Set charger to have searate DC output connectors. (Set for G3-4M or 6M only)',
               'settings.reversedbatterythreshold':'Voltage threshold below which the reversed battery alarm will be triggered (Set for G3 single phase only)',
               'charger.AvailableFixedConfigurations':'Set which nominal battery voltages can be charged by the charger ( Set for G3 single phase only)',
               'framesize.availableframesizes':'List of frame sizes this configuraion is used for',}
advancedInfo = {'powersave.enable':'Allow the charger to shut off modules that are not needed during charging to increase efficiency. For G3 single phase only',
                'powersave.minimumTarget':'Set the per module output power that will cause a charger to shut down a module. For G3-6M only',
                'powersave.maximumTarget':'Set the per module output power that will cause a charger to restart a shut down module. For G3-6M only',
                'modules.maximumvoltage':'Maximum module voltage. For G3 single phase only'}
extraEntry = {'<updatefactoryreset />':'Apply this file to the factory default configuration',
              '<entrylevel />':'Allow this file to be applied to an entry level charger'}
dictList = [regionInfo, acdcInfo, fpInfo, labelInfo, templateInfo, cabinetInfo, advancedInfo, extraEntry]
timeZoneList = ['Australia/Sydney','Pacific/Auckland','America/Los_Angeles','America/New_York','Asia/Tokyo','America/Mexico_City','Europe/London','Europe/Berlin']
localeList = ['en_US', 'en_CA', 'en_NZ', 'de_DE', 'es_419', 'fr_CA', 'fr_FR', 'it_IT', 'ms_MY', 'nl_NL', 'pl_PL', 'pt_BR', 'pt_PT', 'ru_RU', 'sl_SL', 'th_TH', 'tr_TR', 'vi_VN', 'zh_CN']
ulBattList = ['LEAD ACID', 'LEAD ACID,LITHIUM ION']
ulBattOption = ['LEAD ACID', 'LITHIUM ION', 'LEAD ACID,LITHIUM ION']
fixModuleConfigList = ['1x MP1148', '1x MP2248', '1x MP3348', '2x MP3348', '1x MP42', '2x MP42', '1x MP44', '2x MP44', '1x MP46', '2x MP46']
frameSizeList = ['1M', '3M', '4M', '6M']
maxModuleCountList = ['1', '2', '3', '6']
booLeanList = ['true', 'false']
cableNameList = ['1/0AWG', '50mm\u00b2']
cableLengthList = ['2.44', '3']
maxCurrentList = ['48', '85', '120']
regionCbox = [timeZoneList, localeList]
acdcCbox = [booLeanList, booLeanList, cableNameList, cableLengthList, booLeanList]
cabCbox = [frameSizeList, maxModuleCountList, fixModuleConfigList, maxCurrentList, booLeanList]
localeCheckStateList = []
battCheckStateList = []

#customize Qwidget class
'''class cenWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))
        QLabel.setFont(self, QFont('SansSerif', 13))
        #creat box layout to manage layouts within this widget
        hBox = QHBoxLayout()
        self.setLayout(hBox)
        #create a list of main settings
        listWidget = QListWidget(self)
        listWidget.setMinimumWidth(400)
        listWidget.addItems(settingNodes)
        hBox.addWidget(listWidget,0,Qt.AlignLeft)
        #create a widget to populate sub-setting, this widget use grid layout and contain labels and edit txt
        regionWidget = QWidget()
        regionGrid = QGridLayout()
        regionWidget.setLayout(regionGrid)
        #create labels and add into grid
        for key in regionInfo:
            regionLab = QLabel(key, self)
            regionLab.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            regionGrid.addWidget(regionLab)

        hBox.addWidget(regionWidget)
        regionWidget.hide()'''        
#customize tab view widget class
'''class tabWidget(QTabWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        #QLabel.setFont(self, QFont('SansSerif', 13))
        #create widget for each tab
        self.regionTab = QWidget()
        self.acdcTab = QWidget()
        self.fpTab = QWidget()
        self.labelTab = QWidget()
        self.templateTab = QWidget()
        self.cabinetTab = QWidget()
        self.advancedTab = QWidget()
        self.extraTab = QWidget()
        self.newTab = QWidget()
        tabList = [self.regionTab, self.acdcTab, self.fpTab, self.labelTab, self.templateTab, self.cabinetTab, self.advancedTab, self.extraTab, self.newTab]
        for tabs, names in zip(tabList, settingNodes):
            self.addTab(tabs, names)
        self.regionInfoUI()
        self.acdcInfoUI()
        self.fpInfoUI()
        self.labelInfoUI()
        self.templateInfoUI()
        self.cabinetInfoUI()
        self.advancedInfoUI()
        self.extraEntryUI()
        self.addNewNodeUI()

    def regionInfoUI(self):
        layout = QFormLayout()
        for key in regionInfo:
            formLabel = QLabel(key)
            formLabel.setToolTip(regionInfo[key])
            layout.addRow(formLabel, QLineEdit())
        self.regionTab.setLayout(layout)
    
    def acdcInfoUI(self):
        layout = QFormLayout()
        for key in acdcInfo:
            formLabel = QLabel(key)
            formLabel.setToolTip(acdcInfo[key])
            layout.addRow(formLabel, QLineEdit())
        self.acdcTab.setLayout(layout)

    def fpInfoUI(self):
        layout = QFormLayout()
        for key in fpInfo:
            formLabel = QLabel(key)
            formLabel.setToolTip(fpInfo[key])
            layout.addRow(formLabel, QLineEdit())
        self.fpTab.setLayout(layout)
    
    def labelInfoUI(self):
        layout = QFormLayout()
        for key in labelInfo:
            formLabel = QLabel(key)
            formLabel.setToolTip(labelInfo[key])
            layout.addRow(formLabel, QLineEdit())
        self.labelTab.setLayout(layout)

    def templateInfoUI(self):
        layout = QFormLayout()
        for key in templateInfo:
            formLabel = QLabel(key)
            formLabel.setToolTip(templateInfo[key])
            layout.addRow(formLabel, QLineEdit())
        self.templateTab.setLayout(layout)

    def cabinetInfoUI(self):
        layout = QFormLayout()
        for key in cabinetInfo:
            formLabel = QLabel(key)
            formLabel.setToolTip(cabinetInfo[key])
            layout.addRow(formLabel, QLineEdit())
        self.cabinetTab.setLayout(layout)

    def advancedInfoUI(self):
        layout = QFormLayout()
        for key in advancedInfo:
            formLabel = QLabel(key)
            formLabel.setToolTip(advancedInfo[key])
            layout.addRow(formLabel, QLineEdit())
        self.advancedTab.setLayout(layout)

    def extraEntryUI(self):
        layout = QFormLayout()
        for key in extraEntry:
            formLabel = QLabel(key)
            formLabel.setToolTip(extraEntry[key])
            layout.addRow(formLabel, QLineEdit())
        self.extraTab.setLayout(layout)

    def addNewNodeUI(self):
        layout = QHBoxLayout()
        textArea = QTextEdit()
        layout.addWidget(textArea)
        self.newTab.setLayout(layout)
'''
#customize stackedlayout class
'''class stackLO(QStackedLayout):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
'''

#customize MainWindow class
class mainWin(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initWin()

    def initWin(self):
#add status bar to the main window
        #self.statusBar().showMessage('Module Specific Configuration File')
#create menu bar button
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl + Q')
        #exitAct.setStatusTip('Exit Application')
        exitAct.triggered.connect(qApp.quit)
        saveAct = QAction('Save as Config File', self)
        saveAct.setShortcut('Ctrl + S')
        saveAct.triggered.connect(self.createXML)
        #saveAct.setStatusTip('Save Current Settings')
#create menu bar and add above button
        menuBar = self.menuBar()
        exitMenu = menuBar.addMenu('&Exit')
        saveMenu = menuBar.addMenu('&Save to File')
        saveMenu.addAction(saveAct)
        exitMenu.addAction(exitAct)
#create a tab view widget 
        #tabWid = tabWidget()
        #self.setCentralWidget(tabWid)
#set up layout
        mainWidget = QWidget(self)
        vBoxMain = QVBoxLayout()   #layout for the mainWidget
        leftFrame = QListWidget(self)
        leftFrame.addItems(settingNodes)
        leftFrame.setCurrentRow(0)
        leftFrame.itemClicked.connect(self.listClicked)
        rightFrame = QFrame(self)
        rightFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.stackedLO = QStackedLayout()

#create widget for region setting  (check box)
        regionWidget = QWidget()
        regionLayout = QGridLayout()
        #create labels
        self.createLabel(regionInfo, regionLayout)
        #create input line
        self.regEdit = QLineEdit()    
        regionLayout.addWidget(self.regEdit,0,1)
        #create comboBoxes
        self.tzncomBox = self.getBoX(timeZoneList,regionLayout,1)
        self.lncomBox = self.getBoX(localeList,regionLayout,2)
        #create check boxes
        regCheckboxWidget1 = QWidget()
        regCheckboxLO1 = QGridLayout()
        '''regPosiBox1 = [(i, j) for i in range(5) for j in range(4)]
        for position1, locale in zip(regPosiBox1, localeList):
            self.localeCBox = QCheckBox(locale)
            regCheckboxLO1.addWidget(self.localeCBox, *position1)'''
        self.localeChBoxList = CheckBoxListWidget()
        self.localeChBoxList.addItems(localeList)
        regCheckboxLO1.addWidget(self.localeChBoxList)
        regCheckboxWidget1.setLayout(regCheckboxLO1)
        regionLayout.addWidget(regCheckboxWidget1,3,1)
        regionWidget.setLayout(regionLayout)
        self.stackedLO.addWidget(regionWidget)

#create ac dc widget, need tab view (save done)
        acdcWidget = QWidget()
        acdcLayout = QGridLayout()
        #create labels
        self.createLabel(acdcInfo, acdcLayout)
        #create comboBoxes
        self.showACcomBox = self.getBoX(booLeanList,acdcLayout,0)
        self.showDCcomBox = self.getBoX(booLeanList,acdcLayout,1)
        self.cncomBox = self.getBoX(cableNameList,acdcLayout,2)
        self.clcomBox = self.getBoX(cableLengthList,acdcLayout,3)
        self.abpcomBox = self.getBoX(booLeanList,acdcLayout,4)
        #create input line
        self.acdcLineEdit1 = QLineEdit()    
        acdcLayout.addWidget(self.acdcLineEdit1,5,1)
        self.acdcLineEdit2 = QLineEdit()    
        acdcLayout.addWidget(self.acdcLineEdit2,6,1)

        acdcWidget.setLayout(acdcLayout)
        self.stackedLO.addWidget(acdcWidget)

#create widget for front panel setting (save done)
        fpWidget = QWidget()
        fpLayout = QGridLayout()
        self.createLabel(fpInfo, fpLayout)
        self.showRestart = self.getBoX(booLeanList,fpLayout,0)
        self.showRestart.setCurrentIndex(0)
        self.timeOfDay = self.getBoX(booLeanList,fpLayout,1)
        self.timeOfDay.setCurrentIndex(0)
        self.outputTest = self.getBoX(booLeanList,fpLayout,2)
        self.outputTest.setCurrentIndex(0)
        self.startDelay = self.getBoX(booLeanList,fpLayout,3)
        self.startDelay.setCurrentIndex(0)
        self.eualise = self.getBoX(booLeanList,fpLayout,4)
        self.eualise.setCurrentIndex(0)
        fpLayout.setRowStretch(5, 1)
        fpWidget.setLayout(fpLayout)
        self.stackedLO.addWidget(fpWidget)

#create widget for label  (save done)
        labelWidget = QWidget()
        labelLayout = QGridLayout()
        #create labels
        self.createLabel(labelInfo, labelLayout)
        #create comboBox
        self.battTypeComBox = self.getBoX(ulBattList,labelLayout,0)
        #create checkboxes
        labCheckboxWidget = QWidget()
        labCheckboxLO = QVBoxLayout()
        #self.ulBattChBox = QCheckBox('check all')
        self.ulBattChBoxList = CheckBoxListWidget()
        self.ulBattChBoxList.addItems(ulBattOption)
        #self.ulBattChBox.stateChanged.connect(self.ulBattChBoxList.toggleState)
        #labCheckboxLO.addWidget(self.ulBattChBox)
        labCheckboxLO.addWidget(self.ulBattChBoxList)
        labCheckboxWidget.setLayout(labCheckboxLO)
        labelLayout.addWidget(labCheckboxWidget,1,1)
        labelWidget.setLayout(labelLayout)
        self.stackedLO.addWidget(labelWidget)

#create widget for template (save done)
        templateWidget = QWidget()
        templateLayout = QGridLayout()
        #create labels
        self.createLabel(templateInfo, templateLayout)
        #create line eidt
        self.tempName = QLineEdit()
        templateLayout.addWidget(self.tempName,0,1)
        #create text edit
        self.tempList = QTextEdit()
        templateLayout.addWidget(self.tempList,1,1)
        templateWidget.setLayout(templateLayout)
        self.stackedLO.addWidget(templateWidget)

#create widget for cabinet (save done)
        cabWidget = QWidget()
        cabLayout = QGridLayout()
        #create labels
        self.createLabel(cabinetInfo, cabLayout)
        #create line edit
        self.cabInput1 = QLineEdit()
        cabLayout.addWidget(self.cabInput1,0,1)
        #create combobox
        self.fscombBox = self.getBoX(frameSizeList,cabLayout,1)
        self.mmcountcombBox = self.getBoX(maxModuleCountList,cabLayout,2)
        self.fmccombBox = self.getBoX(fixModuleConfigList,cabLayout,3)
        self.mmcurrntcombBox = self.getBoX(maxCurrentList,cabLayout,4)
        self.dccombBox = self.getBoX(booLeanList,cabLayout,5)
        cabWidget.setLayout(cabLayout)
        self.stackedLO.addWidget(cabWidget)

#create widget for Advanced settings (save done)
        advWidget = QWidget()
        advLayout = QGridLayout()
        #create labels
        self.createLabel(advancedInfo, advLayout)
        #create combo box
        self.psComBox = self.getBoX(booLeanList,advLayout,0)
        #create line edit x3
        self.advInput1 = QLineEdit()
        self.advInput2 = QLineEdit()
        self.advInput3 = QLineEdit()
        advLayout.addWidget(self.advInput1, 1, 1)  
        advLayout.addWidget(self.advInput2, 2, 1) 
        advLayout.addWidget(self.advInput3, 3, 1)   
        advLayout.setRowStretch(4, 1)
        advWidget.setLayout(advLayout)
        self.stackedLO.addWidget(advWidget)

#create widget for extra entry (save done)
        entWidget = QWidget()
        entLayout = QVBoxLayout()
        entryLable = QLabel('Please add any extra entry into the below area.\nThe Factory Rest entry will be added into config file automatically.')
        entLayout.addWidget(entryLable)
        self.entryInput = QTextEdit()
        entLayout.addWidget(self.entryInput)
        entWidget.setLayout(entLayout)
        self.stackedLO.addWidget(entWidget)        

#create widget for new node (save done)
        nodeWidget = QWidget()
        nodeLayout = QVBoxLayout()
        nodeLable = QLabel('Please add the new node into the below area.')
        nodeLayout.addWidget(nodeLable)
        self.nodeInput = QTextEdit()
        nodeLayout.addWidget(self.nodeInput)
        nodeWidget.setLayout(nodeLayout)
        self.stackedLO.addWidget(nodeWidget)

#add frame into splitter
        rightFrame.setLayout(self.stackedLO)
        topSplitter = QSplitter(Qt.Horizontal)
        topSplitter.addWidget(leftFrame)
        topSplitter.addWidget(rightFrame)
        topSplitter.setSizes([200, 450])
        vBoxMain.addWidget(topSplitter)
#create Save and Close buttons        
        hBox = QHBoxLayout()
        hBox.addStretch(2)
        closeButton = QPushButton('Close')
        closeButton.clicked.connect(qApp.quit)
        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.settingSave)
        hBox.addWidget(closeButton)
        hBox.addWidget(saveButton)
        vBoxMain.addLayout(hBox)
        mainWidget.setLayout(vBoxMain)
        self.setCentralWidget(mainWidget)
#set main window size and position
        self.resize(700, 550)
        self.setWindowTitle('ConfigEditor')
        self.center()
        self.show()
#function to create label widget
    def createLabel(self, labelDict, widgetLO):
        for dictKey in labelDict.keys():
            widgetLabel = QLabel(dictKey)
            widgetLabel.setToolTip(labelDict[dictKey])
            widgetLO.addWidget(widgetLabel)
#function to create a set of comboboxes according to the given list
    def createComBox(self, ddList, widgetLO, startRow):
        for subList in ddList:    
            newComboBox = QComboBox()
            newComboBox.addItems(subList)
            newComboBox.setCurrentIndex(-1)
            widgetLO.addWidget(newComboBox,startRow,1)
            startRow += 1            
#function to create a single combobox
    def getBoX(self, dList, widgetLO, startRow):
        newBoX = QComboBox()
        newBoX.addItems(dList)
        newBoX.setCurrentIndex(-1)
        widgetLO.addWidget(newBoX,startRow,1)
        return newBoX
#function to check the state of check box
    def chBoxState(self, stateList, optionList):
        print(stateList)
        resultList = []
        for i in range(len(stateList)):
            resultList.append(optionList[stateList[i]])    
        return resultList
#function to switch right hand widgets according to the clicked item in the left hand list
    def listClicked(self, item):
        for i in range(len(settingNodes)):
            if settingNodes[i] == item.text():
                self.stackedLO.setCurrentIndex(i)        
#function to determin screen center point and center the main window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
#function to save settings
    def settingSave(self):
        #Region settings
        configPN = self.regEdit.text() 
        tznVal = self.tzncomBox.currentText()
        lnVal = self.lncomBox.currentText()
        localeCheckStateList = self.chBoxState(self.localeChBoxList.getCheckedRows(), localeList)
        #ACDC settings
        acShow = self.showACcomBox.currentText()
        dcShow = self.showDCcomBox.currentText()
        cableName = self.cncomBox.currentText()
        cableLength = self.clcomBox.currentText()
        autoBP = self.abpcomBox.currentText()
        acThreshold = self.acdcLineEdit1.text()
        acMax = self.acdcLineEdit2.text()
        #FP settings
        dpRestart = self.showRestart.currentText()
        todOverride = self.timeOfDay.currentText()
        dpOPTest = self.outputTest.currentText()
        sdOverride = self.startDelay.currentText()
        eualOverride = self.eualise.currentText()
        #Label settings
        battType = self.battTypeComBox.currentText()
        battCheckStateList = self.chBoxState(self.ulBattChBoxList.getCheckedRows(), ulBattOption)
        #Batt settings
        battTemp = self.tempName.text()
        battTempList = self.tempList.toPlainText()
        #Cabinet settings
        modType = self.cabInput1.text()
        fsVal = self.fscombBox.currentText()
        mmcountVal = self.mmcountcombBox.currentText()
        fmcVal = self.fmccombBox.currentText()
        mmcurrentVal = self.mmcurrntcombBox.currentText()
        dcVal = self.dccombBox.currentText()
        #Advanced settings
        psEnable = self.psComBox.currentText()
        psMin = ''
        psMax = ''
        if psEnable == 'true':
            psMin = self.advInput1.text()
            psMax = self.advInput2.text()
        modMaxV = self.advInput3.text()
        #Extra entry
        extraEntry = self.entryInput.toPlainText()
        #New node
        newNode = self.nodeInput.toPlainText()
        #save to XML
        print(configPN, tznVal, lnVal, localeCheckStateList, acShow, dcShow, cableName,
               cableLength,autoBP, acThreshold, acMax, dpRestart, todOverride, dpOPTest,
               sdOverride, eualOverride, battType, battCheckStateList, battTemp, battTempList,
               modType, fsVal, mmcountVal, fmcVal, mmcurrentVal, dcVal, psEnable, psMin, psMax,
               modMaxV, newNode, extraEntry)
    def createXML(self):
        print('placeholder')
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    ex = mainWin()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()