import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

# Manager
from packages.database.Manager import (
    getAlumnosByGrupo,
    getAllGrupos,
)

# utils
from packages.utils.MessagesResponse import RespBDD

# Models
from packages.database.Models import ModelGrupos


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
        self.getGrupos()
        index = self.grupos_box.findText(grupo,Qt.MatchFixedString)
        if index >= 0:
            self.grupos_box.setCurrentIndex(index)

    # Evento al cerrar la ventana
    def closeEvent(self, event):
        self.__parent.setEnabled(True)
        event.accept()

    # LLama al proceo para actualizar los datos de un alumno
    def actualizaDatos(self):
        pass

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
