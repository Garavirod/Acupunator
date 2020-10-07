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


# Windows
from .Evaluaciones import EvaluacionesWindow

class HistorialesWindow(QMainWindow):
    def __init__(self,parent=None):
        super(HistorialesWindow,self).__init__(parent)
        # Cargamos template del panel de Historiales
        loadUi('templates/Historiales.ui',self)
        # Cargamos los elementos del template
        self.regresar_btn.clicked.connect(lambda: self.backToHome(parent)) 
        self.filtrar_btn.clicked.connect(self.filtrarAlumnos)
        self.table_historial.clicked.connect(self.showHistorial)
        self.getGrupos() #LLena el combo box
        self.filtrarAlumnos() # filtra alumnos y despliega en tabla
        self.__current_group = self.grupos_box.currentText()

    #Regresa a la venta de Panel de control
    def backToHome(self,parent):
        parent.show()
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
    def filtrarAlumnos(self):
        for i in reversed(range(self.table_historial.rowCount())):
            self.table_historial.removeRow(i)
        self.__current_group = self.grupos_box.currentText()
        grupo = ModelGrupos(self.__current_group)
        response = getAlumnosByGrupo(grupo)        
        if not response == RespBDD.ERROR_GET:            
            for registro in response:                
                fullname = "{} {} {}".format(registro[2],registro[1],registro[0])
                boleta = registro[3]
                self.fillTable(self.table_historial,[boleta,fullname])
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar los grupos', QMessageBox.Ok)            

    # Abre una venta con el historial de un alumno especifico
    def showHistorial(self):
        row = self.table_historial.currentRow()
        boleta = self.table_historial.item(row, 0).text()  
        nombre = self.table_historial.item(row, 1).text()
        grupo = self.__current_group
        _evaluacionesWin = EvaluacionesWindow(nombre=nombre,boleta=boleta,grupo=grupo,parent=self)
        print("{} {} {}".format(nombre,boleta,grupo))
        self.hide()
        _evaluacionesWin.show()        
