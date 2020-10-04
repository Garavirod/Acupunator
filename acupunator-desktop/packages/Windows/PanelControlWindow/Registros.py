import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
# Models
from packages.database.Models import (
    ModelAlumno,
    ModelGrupos,
)
# Managers
from packages.database.Manager import (
    registraGrupoAlumnoManager,
)

class RegistrosWindow(QMainWindow):
    
    def __init__(self,parent=None):
        super(RegistrosWindow,self).__init__(parent)
        # Cargamos template del panel de control
        loadUi('templates/Registros.ui',self)        
        # cagrgamos elementos del template
        self.regresar_btn.clicked.connect(lambda:self.backToHome(parent))
        self.guardar_btn.clicked.connect(self.guardaRegistro)        
    #Regresa a la venta de Panel de control
    def backToHome(self,parent):
        parent.showWindowHome()
        self.hide()

    def validaCampos(self):
        if self.nombre_input.text() == "" or self.apma_input.text() == "" or self.appa_input.text() == "" or self.boleta_input.text()=="" or self.grupos_box.currentText()=="":
            return False
        else:
            return True

    # LLama al proeso qeus e encarga de registrar un alumno y asignarlo aun grupo
    def guardaRegistro(self):
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
            print(registraGrupoAlumnoManager(grupo,alumno))
        else:
            self.alert_alumno.setStyleSheet('color: rgb(164,0,0);')
            self.alert_alumno.setText("¡Hay campos vacios!")