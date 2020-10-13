import os
import json
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



class SimuladorWindow(QMainWindow):
    def __init__(self,parent=None):
        super(SimuladorWindow,self).__init__(parent)
        self.__detalle = """
            ¿Desea autorizar la siguiente simulación? \n
            Simulación de tipo : {} \n
            Canal de estudio : {} \n
            Alumno : {} \n
            Boleta : {} \n
            Grupo : {} \n
        """
        # Cargamos template del panel de Simulador
        loadUi('templates/Simulador.ui',self)
        # Cargamos los elementos del template
        self.regresar_btn.clicked.connect(lambda: self.backToHome(parent)) 
        self.filtrar_btn.clicked.connect(self.filtrarAlumnos)
        self.table_alumnos.clicked.connect(self.initAcupunator)
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
        for i in reversed(range(self.table_alumnos.rowCount())):
            self.table_alumnos.removeRow(i)
        self.__current_group = self.grupos_box.currentText()
        grupo = ModelGrupos(self.__current_group)
        response = getAlumnosByGrupo(grupo)        
        if not response == RespBDD.ERROR_GET:            
            for registro in response:                
                fullname = "{} {} {}".format(registro[1],registro[2],registro[0])
                boleta = registro[3]
                self.fillTable(self.table_alumnos,[boleta,fullname])
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar los grupos', QMessageBox.Ok)            

    
    # Generá un arichivo JSON para compartir al simulador
    def generateJSONFile(self,tipo,canal,boleta):
        # ruta a guaradar el arichivo JSON
        path = os.path.dirname(os.path.abspath(__package__))+'/packages/shared/dataShared.json'
        # Estructura del JSON
        data = {}
        data['simulation']=[]
        data['simulation'].append(
            {
                'tipo' : tipo,
                'canal' : canal,
                'numBoleta' : boleta
            }
        )
        with open(str(path), 'w+') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


    # Inicia el proceo de simulación
    def initAcupunator(self):
        row = self.table_alumnos.currentRow()
        boleta = self.table_alumnos.item(row, 0).text()  
        nombre = self.table_alumnos.item(row, 1).text()
        grupo = self.__current_group
        tipo_simulacion = self.tipo_simulacion_box.currentText()
        canal = self.canales_box.currentText()
        # Ventana modal de confirmación
        resp = QMessageBox.question(
            self,
            'Detalle de simulación',
            self.__detalle.format(
                tipo_simulacion,
                canal,
                nombre,
                boleta,
                grupo), 
                QMessageBox.Ok | QMessageBox.Cancel)  
        # Validamos la respesta del suaurio
        if(resp == QMessageBox.Ok):
            # LLamamos al método que creará el arichivo JSON compartdio            
            self.generateJSONFile(tipo_simulacion,canal,boleta)                         
            # Ejecutamos el simulador via CMD