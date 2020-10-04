import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
# Ventanas
from packages.Windows.PanelControlWindow.PanelControl import PanelControlWindow


class LoginWindow(QMainWindow):
    __user__="1234"
    __password__="1234"
    def __init__(self):
        super(LoginWindow,self).__init__()
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
            # Se da acceso a la ventana del panel de control
            _panelcontrol = PanelControlWindow(self)
            _panelcontrol.show()
            self.hide() #Ocultamos la ventana principal            
        else:
            self.label_alert.setText("¡Credenciales incorrectas!")
