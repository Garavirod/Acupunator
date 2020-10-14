import os
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from packages.Windows.LoginWindow.Login import LoginWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([]) #Permite controlar el bucle del programa
    window = LoginWindow()
    window.show()
    app.exec_() #El programa se cerrará inmediatemente al no estar esta linea