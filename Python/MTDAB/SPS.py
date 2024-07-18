import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import matplotlib.pyplot as plt

def main():
    x = np.arange(-11, 11, 1)
    a = 2
    b = 3
    c = 4
    d = 9
    y = a*(x**3) + b*(x**2) + c*x + d 
        
    plt.plot(x, y)
    
    plt.title("Cubic Function")
    plt.xlabel("Values of x")
    plt.ylabel("Values of y")
    plt.show()

if __name__ == '__main__':
    main()