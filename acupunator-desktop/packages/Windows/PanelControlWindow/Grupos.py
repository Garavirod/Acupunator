import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

# Manager
from packages.database.Manager import (
    getFullDataGrupos    
)

# utils
from packages.utils.MessagesResponse import RespBDD


class GruposWindow(QMainWindow):
    def __init__(self,parent=None):
        super(GruposWindow,self).__init__(parent)
        # Cargamos template del panel de Historiales
        loadUi('templates/Grupos.ui',self)
        # Cargamos los elementos del template
        self.regresar_btn.clicked.connect(lambda: self.backTo(parent))                    
        self.getDataGrupos() # trae la info de grupos y despliega en tabla
        

    #Regresa a la venta de Panel de control
    def backTo(self,parent):
        parent.show()
        self.hide()

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
    def getDataGrupos(self):
        for i in reversed(range(self.table_grupos.rowCount())):
            self.table_grupos.removeRow(i)
        # hace la peticion al manager de treer los dadtos del grupo
        response = getFullDataGrupos()
        if not response == RespBDD.ERROR_GET:                              
            for registro in response:                
                grupo = registro[0]
                fecha = registro[1]
                cantidad = registro[2]
                self.fillTable(self.table_grupos,[grupo,fecha,cantidad])
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar los datos', QMessageBox.Ok)            
