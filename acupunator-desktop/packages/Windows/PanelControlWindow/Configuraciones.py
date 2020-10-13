import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

# Models
from packages.database.Models import (
    ModelAlumno,
    ModelGrupos,
    ModelProfesor,
)
# Managers
from packages.database.Manager import (
    eliminaAlumnobyBoleta,
    countAlumnosManager,
    getAlumnosByGrupo,
    getCredencialesAdmin,
    countGruposManager,
    getAllGrupos,
    eliminaDatosGrupoManager,
    actualizaGrupoManager,
    datosGeneralesAdminManager,    
    actualizaDatosAdminManager,
    actualizaPasswordAdminManager
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
        self.cambia_gru_btn.clicked.connect(self.cambiaNombreGrupo)

        # Cargamos los elementos del template tab Mi perfil
        self.__enableInputs = False
        self.setEnableInputs()
        self.cargaDatosAdmin()
        self.editar_btn_Admin.clicked.connect(self.setEnableInputs)
        self.update_admin_dta.clicked.connect(self.actualizaDatosAdmin)
        self.update_admin_psd.clicked.connect(self.actualizaPassword)
        self.regresar_perfil_btn.clicked.connect(lambda:self.backToParent(parent))        

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
            datosAdmin = getCredencialesAdmin()
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
        psd_bdd = getCredencialesAdmin()
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
                            self.password_input_gru.clear()
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

    # Llama al proceso del manager para cambiar nombre de un grupo
    def cambiaNombreGrupo(self):
        new_nombre = self.nuevo_nombre.text()
        psd_auth = self.password_input_gru.text()
        old_nombre= self.grupos_box_gru.currentText()
        
        if new_nombre == "":
            self.alert_auth.setStyleSheet('color: rgb(164,0,0);')
            self.alert_auth.setText("¡No ha colocado el nuevo nombre!") 
        elif psd_auth == "":
            self.alert_auth.setStyleSheet('color: rgb(164,0,0);')
            self.alert_auth.setText("¡Es necesario autorizar la modifiación!")
        else:
            # traemos datos del adminstrador
            psd_bdd = getCredencialesAdmin()
            psd = PasswordEncrypt()
            # Validamos el exito de la petcion de los datos del admin
            if psd_bdd != RespBDD.ERROR_GET and psd_bdd != RespBDD.ERROR_CON:
                # Validamos credenciales
                if psd.validatepassword(psd_auth,psd_bdd[1]):                    
                    response = actualizaGrupoManager(ModelGrupos(old_nombre),new_nombre)
                    if response == RespBDD.SUCCESS:
                        self.getGrupos(self.grupos_box)
                        self.getGrupos(self.grupos_box_gru)                        
                        self.filtraGrupos()
                        self.password_input_gru.clear()
                        QMessageBox.information(self, 'Estado de la petición', '¡Grupo actualizado exitosamente!', QMessageBox.Ok)                                        
                    else:
                        QMessageBox.critical(self, 'Estado de la petición', '¡Error al actualizar datos!', QMessageBox.Ok)                                        
                else:
                    QMessageBox.warning(self, 'Estado de la petición', 'La contraseña no es válida', QMessageBox.Ok)            
            else:                         
                QMessageBox.critical(self, 'Estado de la petición', 'Hubo un error al tratar de validar las credenciales', QMessageBox.Ok)

    """Métodos para la actualización de datos del admin"""             
    def setEnableInputs(self):
        if self.__enableInputs:
            self.nombre_admin_input.setEnabled(True)
            self.appa_admin_input.setEnabled(True)
            self.apma_admin_input.setEnabled(True)
            self.username_input.setEnabled(True)
            self.correo_input.setEnabled(True)          
        else:
            self.nombre_admin_input.setDisabled(True)
            self.appa_admin_input.setDisabled(True)
            self.apma_admin_input.setDisabled(True)
            self.username_input.setDisabled(True)
            self.correo_input.setDisabled(True)
        
        self.__enableInputs = not(self.__enableInputs)       

    def cargaDatosAdmin(self):
        response = datosGeneralesAdminManager()
        if response != RespBDD.ERROR_GET and response != RespBDD.ERROR_CON:
            nombre = response[0]
            apellidoPa = response[1]
            apellidoMa = response[2]
            username = response[3]
            correo =  response[4]
            self.nombre_admin_input.setText(nombre)
            self.appa_admin_input.setText(apellidoPa)
            self.apma_admin_input.setText(apellidoMa)
            self.username_input.setText(username)
            self.correo_input.setText(correo)
        else:
            QMessageBox.critical(self, 'Estado de la petición', 'Hubo un error al cargar los datos', QMessageBox.Ok)

        

    def actualizaPassword(self):
        new_psd = self.new_psd_admin.text() 
        if new_psd != "":
            if self.password_input_admin.text() != "":
                psd_out = self.password_input_admin.text()
                psd_bdd = getCredencialesAdmin()
                if psd_bdd != RespBDD.ERROR_CON and psd_bdd != RespBDD.ERROR_GET:
                    psd_valid = PasswordEncrypt()
                    if psd_valid.validatepassword(psd_out,psd_bdd[1]):                                                
                        # Capturamos la respuesta  de actualización
                        new_psd = psd_valid.encrypt(new_psd)
                        response = actualizaPasswordAdminManager(new_psd)
                        if response == RespBDD.SUCCESS:
                            QMessageBox.information(self, 'Estado de la petición', '¡Datos actualizados exitosamente!', QMessageBox.Ok)                                        
                            self.cargaDatosAdmin()
                            self.__enableInputs=False
                            self.setEnableInputs()
                            self.password_input_admin.clear()
                            self.alert_auth_perfil.setText("")
                            self.new_psd_admin.clear()
                        else:
                            QMessageBox.critical(self, 'Estado de la petición', '¡Error al actualizar datos!', QMessageBox.Ok)                                        
                    else:
                        QMessageBox.critical(self, 'Estado de la petición', 'La contraseña no es válida', QMessageBox.Ok)
                else:
                    QMessageBox.critical(self, 'Estado de la petición', 'Hubo un error al tratar de validar las credenciales', QMessageBox.Ok)
            else:
                self.alert_auth_perfil.setStyleSheet('color: rgb(164,0,0);')
                self.alert_auth_perfil.setText("¡Es necesario autorizar la modifiación!")

        else:
            self.alert_auth_perfil.setStyleSheet('color: rgb(164,0,0);')
            self.alert_auth_perfil.setText("¡No ha colocado el nuevo password!")

        
    # Actualiza los datos del admin
    def actualizaDatosAdmin(self):        
        if not self.__enableInputs:
            if self.nombre_admin_input.text() != "" and self.appa_admin_input.text() != "" and self.apma_admin_input.text() != "" and self.username_input.text() != "" and self.correo_input.text() != "":
                # Vaerificamos campos vacios de autorización
                if self.password_input_admin.text() != "":
                    psd_out = self.password_input_admin.text()
                    psd_bdd = getCredencialesAdmin()
                    if psd_bdd != RespBDD.ERROR_CON and psd_bdd != RespBDD.ERROR_GET:
                        psd_valid = PasswordEncrypt()
                        if psd_valid.validatepassword(psd_out,psd_bdd[1]):
                            # Creaos instancia de profesor
                            profesor = ModelProfesor(
                                self.nombre_admin_input.text(),
                                self.appa_admin_input.text(),
                                self.apma_admin_input.text(),
                                self.username_input.text(),
                                self.correo_input.text()
                            )
                            # Capturamos la respuesta  de actualización
                            response = actualizaDatosAdminManager(profesor)
                            if response == RespBDD.SUCCESS:
                                QMessageBox.information(self, 'Estado de la petición', '¡Datos actualizados exitosamente!', QMessageBox.Ok)                                        
                                self.cargaDatosAdmin()
                                self.__enableInputs=False
                                self.setEnableInputs()
                                self.password_input_admin.clear()
                                self.alert_auth_perfil.setText("")

                            else:
                                QMessageBox.critical(self, 'Estado de la petición', '¡Error al actualizar datos!', QMessageBox.Ok)                                        
                        else:
                            QMessageBox.critical(self, 'Estado de la petición', 'La contraseña no es válida', QMessageBox.Ok)
                    else:
                        QMessageBox.critical(self, 'Estado de la petición', 'Hubo un error al tratar de validar las credenciales', QMessageBox.Ok)

                else:
                    self.alert_auth_perfil.setStyleSheet('color: rgb(164,0,0);')
                    self.alert_auth_perfil.setText("¡Es necesario autorizar la modifiación!")
            else:
                self.alert_auth_perfil.setStyleSheet('color: rgb(164,0,0);')
                self.alert_auth_perfil.setText("¡Hay campos vacios!")