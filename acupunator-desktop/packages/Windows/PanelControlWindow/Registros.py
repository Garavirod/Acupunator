import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

# Models
from packages.database.Models import (
    ModelAlumno,
    ModelGrupos,
)
# Managers
from packages.database.Manager import (
    registraGrupoAlumnoManager,
    registraGrupoManager,
    getAllGrupos,    
)
# utils
from packages.utils.MessagesResponse import RespBDD

from packages.utils.MessagesResponse import *
class RegistrosWindow(QMainWindow):
    
    def __init__(self,parent=None):
        super(RegistrosWindow,self).__init__(parent)
        # Cargamos template del panel de control
        loadUi('templates/Registros.ui',self)        
        # cagrgamos elementos del template
        self.regresar_alu_btn.clicked.connect(lambda:self.backToHome(parent))
        self.guardar_alu_btn.clicked.connect(self.guardaRegistroAlumno)
        self.regresar_gru_btn.clicked.connect(lambda:self.backToHome(parent))
        self.guardar_gru_btn.clicked.connect(self.guardaRegistroGrupo)            
        self.getGrupos()
    #Regresa a la venta de Panel de control
    def backToHome(self,parent):
        parent.showWindowHome()
        self.hide()

    # LLama al prooeso para conseguir tods los grupos en la BDD
    def getGrupos(self):
        response = getAllGrupos()   
        if not response == RespBDD.ERROR_GET:
            self.grupos_box.clear() #Borramos contenido previo
            for gru in response:
                self.grupos_box.addItem(gru[0])
            self.grupos_box.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar los grupos', QMessageBox.Ok)

    def validaCampos(self):
        if self.nombre_input.text() == "" or self.apma_input.text() == "" or self.appa_input.text() == "" or self.boleta_input.text()=="" or self.grupos_box.currentText()=="":
            return False
        else:
            return True

    # LLama al proeso qeus e encarga de registrar un alumno y asignarlo aun grupo
    def guardaRegistroAlumno(self):
        if self.validaCampos():
            # Creamos una instancia de grupo
            grupo = ModelGrupos(self.grupos_box.currentText())
            # Creamos una instancia de alumno
            alumno = ModelAlumno(
                self.nombre_input.text(),
                self.appa_input.text(),
                self.apma_input.text(),
                self.boleta_input.text()
            )
            response = registraGrupoAlumnoManager(grupo,alumno)
            if response == RespBDD.SUCCESS:
                self.nombre_input.clear(),
                self.appa_input.clear(),
                self.apma_input.clear(),
                self.boleta_input.clear()
                QMessageBox.information(self, 'Estado de la petición', 'Registro exitoso', QMessageBox.Ok)
            elif response == RespBDD.EXISTENCE:
                QMessageBox.warning(self, 'Estado de la petición', 'El número de boleta ya existe', QMessageBox.Ok)                
            elif response == RespBDD.ERROR_CON:
                QMessageBox.critical (self, 'Estado de la petición', 'Hubo un error al conectar con la BDD', QMessageBox.Ok)
            else:
                QMessageBox.critical (self, 'Estado de la petición', 'Hubo un error al guardar la información', QMessageBox.Ok)                            
        else:
            self.alert_alumno.setStyleSheet('color: rgb(164,0,0);')
            self.alert_alumno.setText("¡Hay campos vacios!")

    # LLama al proceso para registrar un grupo en la BDD
    def guardaRegistroGrupo(self):
        if not self.grupo_input.text() == "":
            grupo = ModelGrupos(self.grupo_input.text())
            response = registraGrupoManager(grupo)
            if response == RespBDD.SUCCESS:
                self.grupo_input.clear()
                self.getGrupos() #Actualiza la lista de grupos en el combo
                QMessageBox.information(self, 'Estado de la petición', 'Registro exitoso', QMessageBox.Ok)            
            elif  response == RespBDD.EXISTENCE :              
                QMessageBox.warning(self, 'Estado de la petición', 'El grupo ya existe', QMessageBox.Ok)                
            elif response == RespBDD.ERROR_CON:
                QMessageBox.critical (self, 'Estado de la petición', 'Hubo un error al conectar con la BDD', QMessageBox.Ok)
            else:
                QMessageBox.critical (self, 'Estado de la petición', 'Hubo un error al guardar la información', QMessageBox.Ok)                
        else:
            self.alert_grupo.setStyleSheet('color: rgb(164,0,0);')
            self.alert_grupo.setText("¡Hay campos vacios!")

    