
# Modelo Usuario
class ModelUsuario:    
    def __init__(self):
        self.__id=None
        self.__nombreUsuario=None
        self.__apelldioPa=None
        self.__apelldioMa=None    
    #Getters
    def getId(self):
        return self.__id
    def getNombre(self):
        return self.__nombreUsuario
    def getApelldioPa(self):
        return self.__apelldioPa
    def getApellidoMa(self):
        return self.__apelldioMa
    # Setters
    def setId(self,idUsuario):
        self.__id = idUsuario
    def setNombre(self,nombre):
        self.__nombreUsuario = nombre
    def setApelldioPa(self,apellidoPa):
        self.__apelldioPa = apellidoPa
    def setApellidoMa(self,apellidoMa):
        self.__apelldioMa = apellidoMa




class ModelAlumno(ModelUsuario):
    def __init__(self):
        ModelUsuario.__init__(self)
        self.__boleta = None
    
    # Getters
    def getBoleta(self):
        return self.__boleta    
    # Setters
    def setBoleta(self,boleta):
        self.__boleta=boleta



class ModelProfesor(ModelUsuario):
    def __init__(self):
        ModelUsuario.__init__(self)
        self.__username = None
        self.__password = None
        self.__correo = None

    # Getters

    def getUserName(self):
        return self.__username
    
    def getPassword(self):
        return self.__password

    def getCorreo(self):
        return self.__correo

    # Setters

    def setUserName(self,arg):
        self.__username=arg
    
    def setPassword(self,arg):
        self.__password=arg

    def setCorreo(self,arg):
        self.__correo=arg


class ModelGrupos():
    def __init__(self):
        self.__nombreGrupo=None
    
    # Getter
    def setGrupo(self,grupo):
        self.__nombreGrupo=grupo
    # Setter
    def getGrupo(self):
        return self.__nombreGrupo


class ModelEvaluaciones():
    def __init__(self):
        self.__idEvaluacion=None
        self.__puntaje=None
        self.__fecha=None
        self.__modulo=None

    # Getters
    def getIdEvaluacion(self):
        return self.__idEvaluacion
    def getPuntaje(self):
        return self.__puntaje
    def getFecha(self):
        return self.__fecha
    def getModulo(self):
        return self.__modulo

    # Setters

    def setIdEvaluacion(self,arg):
        self.__idEvaluacion=arg
    def setPuntaje(self,arg):
        self.__puntaje=arg
    def setFecha(self,arg):
        self.__fecha=arg
    def setModulo(self,arg):
        self.__modulo=arg