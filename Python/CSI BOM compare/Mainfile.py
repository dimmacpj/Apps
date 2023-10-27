import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from CustWindow import mainWin

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont('Arial', 9))
    ex = mainWin()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
