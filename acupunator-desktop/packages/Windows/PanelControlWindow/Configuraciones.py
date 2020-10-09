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
    eliminaAlumnobyBoleta,
    getDatosProfesorManager,
    getAllGrupos,    
)
# utils
from packages.utils.MessagesResponse import RespBDD
from packages.utils.PsdEncrypt import PasswordEncrypt



class ConfiguracionesWindow(QMainWindow):
    def __init__(self,parent=None):
        super(ConfiguracionesWindow,self).__init__(parent)
        # Cargamos template del panel de control
        loadUi('templates/Configuraciones.ui',self)
        # cagrgamos elementos del template tab Alumnos
        self.elimina_alu_btn.clicked.connect(self.eliminaAlumno)
        self.regresar_alu_btn.clicked.connect(lambda: self.backToParent(parent))
        self.getGrupos()
    
    # LLama al prooeso para conseguir tods los grupos en la BDD
    def getGrupos(self):
        response = getAllGrupos() # hace la petcion al Manager
        if not response == RespBDD.ERROR_GET:
            self.grupos_box.clear() #Borramos contenido previo
            for gru in response:
                self.grupos_box.addItem(gru[0])
            self.grupos_box.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar los grupos', QMessageBox.Ok)

    def backToParent(self,parent):
        parent.show()
        self.hide()
    
    # Métodos para los procesos en el tab Alumno
    def eliminaAlumno(self):
        # Validamos campos vacios
        if not (self.boleta_input.text() == "" and self.password_input.text() == ""):
            # Traemos los datos del admin
            datosAdmin = getDatosProfesorManager()
            if not datosAdmin == RespBDD.ERROR_GET:
                psd = PasswordEncrypt()
                # Validamos password                
                if psd.validatepassword(self.password_input.text(),datosAdmin[1]):
                    # Relizamos la petcion de eliminacion al manager
                    response = eliminaAlumnobyBoleta(self.boleta_input.text())
                    # Verifiamos la respuetsa de psdeliminación de los datos
                    if not response == RespBDD.ERROR_ON_DELETE:
                        QMessageBox.information(self, 'Estado de la petición', 'Alumno eliminado exitosamente', QMessageBox.Ok)                
                    else:
                        QMessageBox.critical(self, 'Estado de la petición', 'No se pudo borrar la infromacion', QMessageBox.Ok)                
                else:
                    self.alert_alumno.setStyleSheet('color: rgb(164,0,0);')
                    self.alert_alumno.setText("El password no es correcto")
            else:
                QMessageBox.warning(self, 'Estado de la petición', 'Error al comporbar credenciales', QMessageBox.Ok)                
        else:
            self.alert_alumno.setStyleSheet('color: rgb(164,0,0);')
            self.alert_alumno.setText("¡Hay campos vacios!")

