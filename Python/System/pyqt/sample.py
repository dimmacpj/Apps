from PyQt5.QtWidgets import QCheckBox, QVBoxLayout, QWidget, QApplication

from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget





class Widget(QWidget):

    def __init__(self):

        super().__init__()

        self.__initUi()



    def __initUi(self):

        allCheckBox = QCheckBox('Check all')

        checkBoxListWidget = CheckBoxListWidget()

        checkBoxListWidget.addItems(['a', 'b', 'c', 'd'])



        allCheckBox.stateChanged.connect(checkBoxListWidget.toggleState)



        lay = QVBoxLayout()

        lay.addWidget(allCheckBox)

        lay.addWidget(checkBoxListWidget)



        self.setLayout(lay)





if __name__ == "__main__":

    import sys



    app = QApplication(sys.argv)

    widget = Widget()

    widget.show()

    app.exec_()