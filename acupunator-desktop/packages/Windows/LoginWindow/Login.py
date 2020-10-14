import os
# Third party apps
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QMovie
# Ventanas
from packages.Windows.PanelControlWindow.PanelControl import PanelControlWindow
# Manager
from packages.database.Manager import getCredencialesAdmin
# Utils
from packages.utils.PsdEncrypt import PasswordEncrypt
from packages.utils.RecoverPassword import RecoverPassword

class LoginWindow(QMainWindow):    
    def __init__(self):
        super(LoginWindow,self).__init__()
        self.__user=None
        self.__password=None
        # Cargamos template
        loadUi('templates/Login.ui',self)
        # Componentes del template
        self.password_btn.clicked.connect(self.recoverPsd)
        self.login_btn.clicked.connect(self.validaCredenciales)
        path = os.path.dirname(os.path.abspath(__package__))+'/img/tindaleffect.gif'
        self.movie = QMovie(str(path))
        self.tindal.setMovie(self.movie)
        self.movie.start()

    
    
    # Valida las credenciales del usuario
    def validaCredenciales(self):        
        # Credenciaes del front
        user = self.user_input.text()
        password = self.password_input.text()
        # hasheamos el psd del front
        psd = PasswordEncrypt()
        password = psd.encrypt(password)
        self.label_alert.setStyleSheet('color: rgb(164,0,0);')
        self.label_alert.setStyleSheet('background-color:none;')
        if (user == "" or password=="" ):            
            self.label_alert.setText("¡Hay campos vacios!")
        else:
            # Credenciales de la BDD
            credenciales = getCredencialesAdmin()
            self.__user = credenciales[0]
            self.__password = credenciales[1]
            if (user==self.__user) and (password==self.__password):
                # Se da acceso a la ventana del panel de control
                _panelcontrol = PanelControlWindow(self)
                _panelcontrol.show()
                self.hide() #Ocultamos la ventana principal            
            else:
                self.label_alert.setText("¡Credenciales incorrectas!")

    # Manda notifición con nuevo password y username
    def recoverPsd(self):
        self.password_btn.setDisabled(True)        
        notifiaction = RecoverPassword()
        resp = notifiaction.sendNotification()
        if resp:
            QMessageBox.information(self, 'Estado de la petición', 'Se mandaron nuevas credenciales a su email', QMessageBox.Ok)                
        else:
            QMessageBox.critical(self, 'Estado de la petición', 'No se pudieron mandar nuevas credenciales', QMessageBox.Ok)
        self.password_btn.setEnabled(True)                   