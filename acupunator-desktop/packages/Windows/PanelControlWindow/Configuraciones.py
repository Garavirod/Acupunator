import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
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
    countAlumnosManager,
    getAlumnosByGrupo,
    getDatosProfesorManager,
    countGruposManager,
    getAllGrupos,
    eliminaDatosGrupoManager,    
)
# utils
from packages.utils.MessagesResponse import RespBDD
from packages.utils.PsdEncrypt import PasswordEncrypt


# windows
from .ActualizaAlumno import ActualizaAlumnoWindow



class ConfiguracionesWindow(QMainWindow):
    def __init__(self,parent=None):
        super(ConfiguracionesWindow,self).__init__(parent)        
        # Cargamos template del panel de control
        loadUi('templates/Configuraciones.ui',self)
        # cagrgamos elementos del template tab Alumnos        
        self.elimina_alu_btn.clicked.connect(self.eliminaAlumno)
        self.regresar_alu_btn.clicked.connect(lambda: self.backToParent(parent))
        self.filtro_btn_alumno.clicked.connect(self.filtraGrupos)
        self.table_alumnos.clicked.connect(lambda:self.showActualizaDatos(parent))
        self.__current_group = None
        self.getGrupos(self.grupos_box)
        self.countAlumnos()
        self.filtraGrupos()

        # Cargamos elementos del template tab grupo
        self.regresar_gru_btn.clicked.connect(lambda: self.backToParent(parent))
        self.countGrupos()
        self.getGrupos(self.grupos_box_gru)
        self.elimina_gru_btn.clicked.connect(self.eliminaDatosGrupo)

    # LLama al prooeso para conseguir tods los grupos en la BDD
    def getGrupos(self,combo):
        response = getAllGrupos() # hace la petcion al Manager
        if not response == RespBDD.ERROR_GET:
            combo.clear() #Borramos contenido previo
            for gru in response:
                combo.addItem(gru[0])
            combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar los grupos', QMessageBox.Ok)

    # Regresa a la ventana padre
    def backToParent(self,parent):
        parent.show()
        self.hide()

    # LLama al proceso del manager que cuenta el numero de alumnos
    def countAlumnos(self):
        response = countAlumnosManager()
        if response != RespBDD.ERROR_GET:
            print(response[0])
            self.label_num_alum.setText(str(response[0]))
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar el numero de alumnos', QMessageBox.Ok)                



      # Agrega datos a una tabla QTableWidget
    def fillTable(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            cell.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            table.setItem(row, col, cell)
            col += 1


    # Filtrar grupo
    def filtraGrupos(self):
        # Borramos conetdo de la tabla
        for i in reversed(range(self.table_alumnos.rowCount())):
            self.table_alumnos.removeRow(i)
        # Capturamos el grupo del combobox
        self.__current_group = self.grupos_box.currentText()
        # Creamos una instanica de grupo
        grupo = ModelGrupos(self.__current_group)
        # Hacemos la petcion al Manager de los alumno en ese grupo
        response = getAlumnosByGrupo(grupo)
        if not response == RespBDD.ERROR_GET:            
            for registro in response:                
                fullname = "{} {} {}".format(registro[1],registro[2],registro[0])
                boleta = registro[3]
                self.fillTable(self.table_alumnos,[boleta,fullname])
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar los grupos', QMessageBox.Ok)            



    
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
                        self.boleta_input.clear()
                        self.password_input.clear()
                        self.countAlumnos()
                        self.filtraGrupos()
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

    # Abre una ventana con los datos del alumno
    def showActualizaDatos(self,parent):
        row = self.table_alumnos.currentRow()
        boleta = self.table_alumnos.item(row, 0).text()  
        nombre = self.table_alumnos.item(row, 1).text()
        grupo = self.__current_group        
        print("{} {} {}".format(nombre,boleta,grupo))
        # Destructuramos el nombre en sus partes
        nombre = nombre.split(" ")
        # Inhabilitamos la ventana padre para evitar procesos simultaneos
        self.setEnabled(False)
        # Creamos la instacia de la Ventana que servirá para actucalizar los datos
        windActualizaDatos = ActualizaAlumnoWindow(
            parent=self,
            nombre=nombre[2],
            boleta=boleta,
            apellidoPa=nombre[0],
            apellidoMa=nombre[1],
            grupo=grupo)
        # Mostramos la ventana
        windActualizaDatos.show()

    """Métodos para la sección de eliminacion y actualización de grupos"""
    def countGrupos(self):
        numGrupos = countGruposManager()
        if numGrupos != RespBDD.ERROR_GET and numGrupos != RespBDD.ERROR_CON:
            self.label_num_grupos.setText(str(numGrupos[0]))
        else:
            QMessageBox.warning(self, 'Estado de la petición', 'Error al cargar el numero de grupos', QMessageBox.Ok)                

    # Llama a los proceso del manager para elimanr datso relacionados a un grupo
    def eliminaDatosGrupo(self):
        psd_auth = self.password_input_gru.text()
        psd_bdd = getDatosProfesorManager()
        current_gru= self.grupos_box_gru.currentText()
        # Valiamos que el input no esta vacio
        if not psd_auth == "":
            if psd_bdd != RespBDD.ERROR_GET and psd_bdd != RespBDD.ERROR_CON:
                # Validamos credenciales
                psd = PasswordEncrypt()
                if psd.validatepassword(psd_auth,psd_bdd[1]):
                    # Eliminanos grupo o alumnos del grupo
                    grupo = ModelGrupos(current_gru)
                    if self.radio_grupo.isChecked():
                        # Eliminamos grupo completo
                        response = eliminaDatosGrupoManager(grupo,False)
                        if response == RespBDD.SUCCESS:
                            self.countGrupos()
                            self.getGrupos(self.grupos_box_gru)
                            self.getGrupos(self.grupos_box)
                            QMessageBox.information(self, 'Estado de la petición', '¡Grupo eliminado exitosamente!', QMessageBox.Ok)                                        
                        else:                            
                            QMessageBox.information(self, 'Estado de la petición', '¡Error al eliminar el grupo!', QMessageBox.Ok)                                        

                    # Eliminamos sólo alumnos del grupo
                    else:
                        response = eliminaDatosGrupoManager(grupo,True)
                        if response == RespBDD.SUCCESS:
                            self.getGrupos(self.grupos_box)
                            self.countAlumnos()
                            self.filtraGrupos()
                            QMessageBox.information(self, 'Estado de la petición', '¡Alumnos dados de baja exitosamente!', QMessageBox.Ok)            
                        else:
                            QMessageBox.information(self, 'Estado de la petición', '¡Error al dar de baja alumnos!', QMessageBox.Ok)                                        
                    
                else:
                    QMessageBox.warning(self, 'Estado de la petición', 'La contraseña no es válida', QMessageBox.Ok)            

            else:
                QMessageBox.critical(self, 'Estado de la petición', 'Hubo un error al tratar de validar las credenciales', QMessageBox.Ok)            
        else:
            self.alert_auth.setStyleSheet('color: rgb(164,0,0);')
            self.alert_auth.setText("¡Es necesario autorizar la modifiación!")            
