import os.path
import sqlite3
from sqlite3 import Error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Crea una conexión con la base de datos y la retorna
def connectionDBManager():
    conn = None
    db_path = os.path.join(BASE_DIR, "AcupunatorDB.db")
    try:
        conn = sqlite3.connect(db_path)        
    except Error:
        print ("Hubo un error al conectar con las base de datos")
    return conn


# Registrar un alumno en el sistema
def registraAlumnoManager(alumno):    
    conn = connectionDBManager()       
    if not conn == None:
        try:
            cursor = conn.cursor()
            nombre = alumno.getNombre()
            apellidoPa =alumno.getApelldioPa()
            apellidoMa =alumno.getApellidoMa()
            # Consulta para registrar un usuario
            query = 'INSERT INTO "Usuario" (nombre,apellidoPa,apellidoMa) VALUES ("{}","{}","{}")'.format(nombre,apellidoPa,apellidoMa)
            cursor.execute(query)        
            # Confirmamos cambios en la BDD
            conn.commit()
            # Consulta para registar a un alumno
            query= 'INSERT INTO "Alumno" VALUES ("{}",last_insert_rowid())'.format(alumno.getBoleta())                       
            cursor.execute(query)
            # Confirmamos cambios en la BDD
            conn.commit()
            # Cerramos la conexión con la BDD
            conn.close()
            return True
        except Error:
            print("HUBO UN ERROR DE TIPO",Error)
            return False
        
    else:
        return False
        


# Registra un grupo en el sistema
def registraGrupoManager(grupo):
    conn = connectionDBManager()
    if not conn == None:
        cursor = conn.cursor()
        # Consulta para registar un grupo en el sistema
        query= 'INSERT INTO "Grupo" VALUES ("{}")'.format(grupo)                       
        cursor.execute(query)
        # Confirmamos cambios en la BDD
        conn.commit()
        # Cerramos la conexión con la BDD
        conn.close()
        return True
    else:
        return False

    
# Registra un alumno en un grupo

def registraGrupoAlumnoManager(grupo,alumno):
    responseAlumno = registraAlumnoManager(alumno)    
    conn = connectionDBManager()
    if not (conn == None) and (responseAlumno != False):
        cursor = conn.cursor()
        query = 'INSERT INTO "Grupo_Alumno" VALUES ("{}","{}")'.format(grupo.getGrupo(),alumno.getBoleta())        
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    else:
        return False

