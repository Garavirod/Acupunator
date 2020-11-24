import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
# Ventanas
from . import (
    Registros,
    Historiales,
    Alumnos,
    Grupos,
    Configuraciones,
    Simulador,
)

# Manager
from packages.database.Manager import getCredencialesAdmin

class PanelControlWindow(QMainWindow):
    def __init__(self,parent=None):
        super(PanelControlWindow,self).__init__(parent)
        # Cargamos template del panel de control
        loadUi('templates/Home.ui',self)
        # cargamos elementos del template
        self.setUserName()
        self.logout.clicked.connect(lambda:self.cerrarSesion())
        self.registro_btn.clicked.connect(lambda:self.openSectionPanel("Registro"))
        self.historial_btn.clicked.connect(lambda: self.openSectionPanel("Historiales"))
        self.alumnos_btn.clicked.connect(lambda:self.openSectionPanel("Alumnos"))
        self.grupos_btn.clicked.connect(lambda:self.openSectionPanel("Grupos"))
        self.settings_btn.clicked.connect(lambda: self.openSectionPanel("Configuraciones"))
        self.simulador_btn.clicked.connect(lambda: self.openSectionPanel("Simulador"))
        
    # Abre la ventana e una sección dependiendo cual se eligó
    def openSectionPanel(self,sectionName):
        _sectionWindow = None
        if sectionName == "Registro":
            _sectionWindow = Registros.RegistrosWindow(self)                        
        elif sectionName == "Historiales":
            _sectionWindow = Historiales.HistorialesWindow(self)        
        elif sectionName == "Simulador":
            _sectionWindow = Simulador.SimuladorWindow(self)
        elif sectionName == "Grupos":
            _sectionWindow = Grupos.GruposWindow(self)        
        elif sectionName == "Alumnos":
            _sectionWindow = Alumnos.AlumnosWindow(self)            
        else:
            _sectionWindow = Configuraciones.ConfiguracionesWindow(self)
        self.hide()
        _sectionWindow.show()    

    # Cierra la sesión de la aplicación
    def cerrarSesion(self):
        resp = QMessageBox.question(self,'cerrar sesión',"¿Seguro que desea salir?", QMessageBox.Ok | QMessageBox.Cancel)
        if resp == QMessageBox.Ok:
            self.close()
    
    # Mostarr nombre de usuario actual
    def setUserName(self):
        username = getCredencialesAdmin()        
        self.label_username.setText(str(username[0]))