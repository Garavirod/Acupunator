import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class HistorialesWindow(QMainWindow):
    def __init__(self,parent=None):
        super(HistorialesWindow,self).__init__(parent)
        # Cargamos template del panel de Historiales
        loadUi('templates/Historiales.ui',self)
        # Cargamos los elementos del template
        self.regresar_btn.clicked.connect(lambda: self.backToHome(parent)) 
        self.filtrar_btn.clicked.connect(lambda: self.filtrarAlumnos(grupo="3CM3"))

    #Regresa a la venta de Panel de control
    def backToHome(self,parent):
        parent.showWindowHome()
        self.hide()

    # Filtrar alumnos

    def filtrarAlumnos(self,grupo):
        pass