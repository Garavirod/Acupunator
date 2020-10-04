import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class RegistrosWindow(QMainWindow):
    
    def __init__(self,parent=None):
        super(RegistrosWindow,self).__init__(parent)
        # Cargamos template del panel de control
        loadUi('templates/Registros.ui',self)        
        # obtenemos botones del template
        self.regresar_btn.clicked.connect(lambda:self.backToHome(parent))
    #Regresa a la venta de Panel de control
    def backToHome(self,parent):
        parent.showWindowHome()
        self.hide()