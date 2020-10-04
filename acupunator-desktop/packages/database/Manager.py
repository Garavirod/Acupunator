import sqlite3
from sqlite3 import Error
# models
from .Models import (
    ModelAlumno,
    ModelProfesor,
)

def connectionDB():
    conn = None
    try:
        conn = sqlite3.connect('AcupunatorDB.db')        
    except Error:
        print ("Hubo un error al conectar con las base de datos")
    return conn

def registraUsuario(rol,user):
    conn = connectionDB()
    query = ""
    if(conn != None):
        nombre = user.getNombre()
        apellidoPa =user.getApelldioPa()
        apellidoMa =user.getApellidoMa()
        cursor = conn.cursor()
        query = "INSERT INTO Usuario (nombre,apellidoPa,apellidoMa) VALUES({},{},{});".format(nombre,apellidoPa,apellidoMa)
        cursor.execute(query)
        if rol == "Alumno":
            boleta = user.getBoleta()
            query= "INSERT INTO Alumno VALUES({},last_insert_rowid());".format(boleta)                       
            cursor.execute(query)            
        else:
            pass
        conn.close()

        
    
