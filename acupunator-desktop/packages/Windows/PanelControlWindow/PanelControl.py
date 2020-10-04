import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
# Ventanas
from .Registros import RegistrosWindow

class PanelControlWindow(QMainWindow):
    def __init__(self,parent=None):
        super(PanelControlWindow,self).__init__(parent)
        # Cargamos template del panel de control
        loadUi('templates/Home.ui',self)
        # obtenemos botones del template Pnale de control
        self.logout.clicked.connect(lambda:self.cerrarSesion())
        self.registro_btn.clicked.connect(lambda:self.openSectionPanel("Registro"))
    
    def openSectionPanel(self,sectionName):
        _sectionWindow = None
        if sectionName == "Registro":
            _sectionWindow = RegistrosWindow(self)                        
        elif sectionName == "Historiales":
            pass
        elif sectionName == "Simulador":
            pass
        elif sectionName == "Grupos":
            pass
        elif sectionName == "Alumnos":
            pass
        else:
            pass
        self.hide()
        _sectionWindow.show()
    
    # Esta función se llama desde otra ventana para volverla a mostrar
    def showWindowHome(self):
        self.show()


    # Cierra la sesión de la aplicación
    def cerrarSesion(self):
        self.close()