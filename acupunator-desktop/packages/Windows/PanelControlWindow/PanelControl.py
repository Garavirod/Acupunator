import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
# Ventanas
from . import (
    Registros,
    Historiales,
)

class PanelControlWindow(QMainWindow):
    def __init__(self,parent=None):
        super(PanelControlWindow,self).__init__(parent)
        # Cargamos template del panel de control
        loadUi('templates/Home.ui',self)
        # cargamos elementos del template
        self.logout.clicked.connect(lambda:self.cerrarSesion())
        self.registro_btn.clicked.connect(lambda:self.openSectionPanel("Registro"))
        self.historial_btn.clicked.connect(lambda: self.openSectionPanel("Historiales"))
    # Abre la ventana e una sección dependiendo cual se eligó
    def openSectionPanel(self,sectionName):
        _sectionWindow = None
        if sectionName == "Registro":
            _sectionWindow = Registros.RegistrosWindow(self)                        
        elif sectionName == "Historiales":
            _sectionWindow = Historiales.HistorialesWindow(self)
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