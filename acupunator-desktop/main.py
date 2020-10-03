import os
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from packages.LoginWindow.Login import Login

if __name__ == "__main__":
    app = QtWidgets.QApplication([]) #Permite controlar el bucle del programa
    window = Login()
    window.show()
    app.exec_() #El programa se cerrará inmediatemente al no estar esta linea