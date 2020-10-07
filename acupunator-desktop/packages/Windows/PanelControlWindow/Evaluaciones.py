import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


# Manager
from packages.database.Manager import (
    getEvaluaciones
)

# utils
from packages.utils.MessagesResponse import RespBDD

# Models
from packages.database.Models import ModelGrupos

class EvaluacionesWindow(QMainWindow):
    def __init__(self,parent=None,nombre,boleta,grupo):
        super(EvaluacionesWindow,self).__init__(parent)
        # Cargamos los datos del alumno
        self.__nombre_alumno = nombre
        self.__boleta = boleta
        self.__grupo = grupo
        # Cargamos template del panel de Historiales
        loadUi('templates/Evaluaciones.ui',self)
        # Cargamos los elementos del template
        self.regresar_btn.clicked.connect(lambda: self.backTo(parent))        
        self.name_label.setText(self.__nombre_alumno)
        self.boleta_label.setText(self.__boleta)
        self.grupo_label.setText(self.__grupo)
        self.showEvaluaciones() # filtra alumnos y despliega en tabla
        

    #Regresa a la venta de Panel de control
    def backTo(self,parent):
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


    # Agrega datos a una tabla
    def fillTable(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            cell.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            table.setItem(row, col, cell)
            col += 1

    # Filtrar alumnos por grupo
    def showEvaluaciones(self):
        # Vaciamos la tabla previamente
        for i in reversed(range(self.table_evaluaciones.rowCount())):
            self.table_evaluaciones.removeRow(i)
        self.__current_group = self.grupos_box.currentText()
        # Hacemos la petcion  a la BDD
        response = getEvaluaciones(self.__boleta)
        # si la peticion fue exitosa se proce a llenar tabla
        if not response == RespBDD.ERROR_GET:
            row = 0 
            for registro in response:
                col = 0                
                self.fillTable(self.table_evaluaciones,[registro[0],registro[1],registro[2]])
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar las evaluaciones', QMessageBox.Ok)            
