import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

# Manager
from packages.database.Manager import (
    getAlumnosByGrupo,
    getAllGrupos,
    actualizaAlumnoManager,
)

# utils
from packages.utils.MessagesResponse import RespBDD

# Models
from packages.database.Models import ModelGrupos, ModelAlumno


class ActualizaAlumnoWindow(QMainWindow):
    def __init__(self,nombre,boleta,apellidoPa,apellidoMa,grupo,parent=None):
        self.__parent = parent
        super(ActualizaAlumnoWindow,self).__init__(self.__parent)
        # Cargamos template del panel de Historiales
        loadUi('templates/ActualizaDatosAlumno.ui',self)
        # Cargamos los elementos del template
        self.regresar_alu_btn.clicked.connect(self.close)
        self.guardar_alu_btn.clicked.connect(self.actualizaDatos)
        self.nombre_input.setText(nombre)
        self.boleta_input.setText(boleta)
        self.appa_input.setText(apellidoPa)
        self.apma_input.setText(apellidoMa)
        self.__oldBoleta = boleta
        self.getGrupos()
        index = self.grupos_box.findText(grupo,Qt.MatchFixedString)
        if index >= 0:
            self.grupos_box.setCurrentIndex(index)

    # Evento al cerrar la ventana
    def closeEvent(self, event):
        self.__parent.setEnabled(True)
        event.accept()

    # LLama al proceso para actualizar los datos de un alumno
    def actualizaDatos(self):
        if not (self.nombre_input.text()=="" and self.boleta_input.text()=="" and self.appa_input.text() =="" and self.apma_input.text()==""):
            # Creamos instancia de alumno
            alumno = ModelAlumno(
                self.nombre_input.text(),
                self.appa_input.text(),
                self.apma_input.text(),
                self.boleta_input.text()
            )
            # Creamos instancia de grupo
            grupo = ModelGrupos(self.grupos_box.currentText())
            # LLamamos al proceso del Manager que actualiza los datos del alumno
            response = actualizaAlumnoManager(alumno,grupo,self.__oldBoleta)
            if not response == RespBDD.ERROR_ON_UPDATE:
                QMessageBox.information(self, 'Estado de la petición', 'Datos actualizados exitosamente', QMessageBox.Ok)                
                self.__parent.filtraGrupos()
            else:
                QMessageBox.critical(self, 'Estado de la petición', 'Error al actualizar datos', QMessageBox.Ok)

        else:
            self.label_alert.setStyleSheet('color: rgb(164,0,0);')
            self.label_alert.setText("¡Hay campos vacios!")            

     # LLama al proceso para conseguir todos los grupos en la BDD
    def getGrupos(self):
        response = getAllGrupos()   
        if not response == RespBDD.ERROR_GET:
            self.grupos_box.clear() #Borramos contenido previo
            for gru in response:
                self.grupos_box.addItem(gru[0])
            self.grupos_box.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar los grupos', QMessageBox.Ok)
