import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class Login(QMainWindow):
    __user__="1234"
    __password__="1234"
    def __init__(self):
        super(Login,self).__init__()
        # Cargamos template
        loadUi('templates/Login.ui',self)
        # Componentes del template
        self.login_btn.clicked.connect(self.validaCredenciales)
    
    # Valida las credenciales del usuario
    def validaCredenciales(self):
        user = self.user_input.text()
        password = self.password_input.text()
        self.label_alert.setStyleSheet('color: rgb(164,0,0);')
        if (user == "" or password=="" ):            
            self.label_alert.setText("¡Hay campos vacios!")
        elif (user==self.__user__) and (password==self.__password__):
            # parametros = ParametrosWindow(self)
            # parametros.show()
            # self.hide()
            self.label_alert.setStyleSheet('color: rgb(78,154,6);')
            self.label_alert.setText("¡Credenciales correctas!")
        else:
            self.label_alert.setText("¡Credenciales incorrectas!")
