from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
# Manager
from packages.database.Manager import (
    getCredencialesAdmin,
    updateCredentialsManager,
)
# utils
from packages.utils.MessagesResponse import RespBDD
from packages.utils.PsdEncrypt import PasswordEncrypt

class RecoverPassword:
    def __init__(self):
        self.__emisor = "acupunator@gmail.com"
        self.__receptor = ""
        self.__mensaje = ""
        self.__password = 'acupunator!"#'
        self.__new_psd = ""
        self.__new_psd_hash = ""
        self.__new_username = ""

    def generateNewCredentials(self):
        # consjunto de caracteres ascci para fromar password y username
        nums = set(range(65,123))
        nums = nums - {91,92,93,94,95,96}
        nums = list(nums)
        
        # Genera password aleatorio
        for i in range(8):
            self.__new_psd += chr(nums[random.randint(0,len(nums)-1)])
        
        # Hashea nuevo password
        psd = PasswordEncrypt()
        self.__new_psd_hash = psd.encrypt(self.__new_psd)
        
        # Genera nuevo username
        for i in range(5):
            self.__new_username += chr(nums[random.randint(0,len(nums)-1)])


    # consigue el correo actual de admisntrador
    def getCorreoAdmin(self):
        data = getCredencialesAdmin()
        if data != RespBDD.ERROR_GET and data != RespBDD.ERROR_CON:
            return {'success':True, 'msg':data[2]}
        else:
            return {'success':False, 'msg':'Error al traer email'}


    # Cambia el nombre de usuario y contraseña en la BDD
    def changeCredentials(self):        
        response = updateCredentialsManager(self.__new_psd_hash,self.__new_username)
        if response == RespBDD.SUCCESS:
            return True
        else:
            return False


    # Manda la notifiación al correo del admin
    def sendNotification(self):
        # Configuracion del mail 
        text = """
            Acupunator.\n
            Solicitud de recuperación de claves. \n
            Sus nuevas credenciales de acceso son:\n
            username : {}
            password : {}
        """        
        # Conseguimos el correo del adminstrador
        correo_receptor = self.getCorreoAdmin()

        # Si hubo éxito en conseguirlo, llenamos el mail
        if correo_receptor['success']:
            # Generamos nuevas credenciales
            self.generateNewCredentials()
            print(" psd {} \n username {} ".format(self.__new_psd,self.__new_username))
            # Damos formato al correo
            self.__receptor = correo_receptor['msg']
            self.__mensaje = MIMEText(text.format(self.__new_username,self.__new_psd)) 
            self.__mensaje['From']=self.__emisor 
            self.__mensaje['To']=self.__receptor 
            self.__mensaje['Subject']="Recuperación de claves ACUPUNATOR" 

            # Cambiamos credenicales en la BDD
            if self.changeCredentials():                                           
                # Nos conectamos al servidor SMTP de Gmail
                try:                    
                    serverSMTP = smtplib.SMTP('smtp.gmail.com',587) 
                    serverSMTP.ehlo() 
                    serverSMTP.starttls() 
                    serverSMTP.ehlo() 
                    serverSMTP.login(self.__emisor,self.__password) 
                    
                    # Enviamos el mensaje 
                    serverSMTP.sendmail(self.__emisor,self.__receptor,self.__mensaje.as_string()) 
                        
                    # Cerramos la conexion 
                    serverSMTP.close() 
                    return True
                except:
                    return False                    
            else:
                return False
        else:
            return False