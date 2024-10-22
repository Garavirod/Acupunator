import os.path
import sqlite3
from sqlite3 import Error
# Path de la BDD
BASE_DIR = os.path.dirname(os.path.abspath(__package__))+"/packages/simulator/"
# Respuestas a peticiones de la BDD
from packages.utils.MessagesResponse import RespBDD;

# Crea una conexión con la base de datos y la retorna
def connectionDBManager():
    conn = RespBDD.ERROR_CON
    db_path = os.path.join(BASE_DIR, "AcupunatorDB.db")
    try:
        conn = sqlite3.connect(db_path)
        # Habilitamos llaves foraneas, Sqlite no las habilita por defecto
        conn.execute("PRAGMA foreign_keys = 1")        
    except Error:
        print ("Hubo un error al conectar con las base de datos")
    return conn


# Verifia la existencia de un alumno dado el numero de boleta
def verifyExistenceAlumno(boleta):
    conn = connectionDBManager()    
    if not conn == None:
        try:
            cursor=conn.cursor()
            query = 'SELECT * FROM "Alumno" WHERE numBoleta = "{}"'.format(boleta)
            cursor.execute(query)
            rows = cursor.fetchone()
            if rows:
                return True
            else:
                return False
        except Error:
            print("Error alverificar la existencia del usuario")

# Verifica la existencia de un grupo en las base de datos
def verfyExistenceGrupo(grupo):
    conn = connectionDBManager()    
    if not conn == None:
        try:
            cursor=conn.cursor()
            query = 'SELECT * FROM "Grupo" WHERE nombreGrupo = "{}"'.format(grupo)
            cursor.execute(query)
            rows = cursor.fetchone()
            if rows:
                return True
            else:
                return False
        except Error:
            print("Error al verificar la existencia del usuario")

# Registrar un alumno en el sistema
def registraAlumnoManager(alumno):    
    conn = connectionDBManager()         
    if not conn == RespBDD.ERROR_CON:
            exist = verifyExistenceAlumno(alumno.getBoleta())
            if not exist:
                try:
                    cursor = conn.cursor()
                    # Datos del alumno
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
                    return RespBDD.SUCCESS
                except Error:
                    print("Error al registrar al usuario alumno ",Error)
                    return RespBDD.ERROR_ON_SAVE                    
            else:                
                return RespBDD.EXISTENCE
    else:
        return RespBDD.ERROR_CON
        

# Registra un grupo en el sistema
def registraGrupoManager(grupo):
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            exist = verfyExistenceGrupo(grupo.getGrupo())
            if not exist:
                cursor = conn.cursor()
                # Consulta para registar un grupo en el sistema
                query= 'INSERT INTO "Grupo" VALUES("{}","{}")'.format(grupo.getGrupo(),grupo.getFechaCreacion())                       
                cursor.execute(query)
                # Confirmamos cambios en la BDD
                conn.commit()
                # Cerramos la conexión con la BDD
                conn.close()
                return RespBDD.SUCCESS
            else:
                return RespBDD.EXISTENCE            
        except Error as err:
            print("Error al insertar el grupo",str(err))
            return RespBDD.ERROR_ON_SAVE
    else:
        return RespBDD.ERROR_CON

    
# Registra un alumno en un grupo
def registraGrupoAlumnoManager(grupo,alumno):
    responseAlumno = registraAlumnoManager(alumno)    
    conn = connectionDBManager()
    if not (conn == RespBDD.ERROR_CON) and (responseAlumno == RespBDD.SUCCESS):
        try:
            cursor = conn.cursor()
            query = 'INSERT INTO "Grupo_Alumno" VALUES ("{}","{}")'.format(grupo.getGrupo(),alumno.getBoleta())        
            cursor.execute(query)
            conn.commit()
            conn.close()
            return RespBDD.SUCCESS           
        except expression as identifier:
            return RespBDD.ERROR_ON_SAVE
    else:
        return responseAlumno


# Traeer todos los grupos regisrados


def getAllGrupos():
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            cursor=conn.cursor()
            query = 'SELECT * FROM "Grupo"'
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Error as err:
            print("Error al verificar los grupos",str(err))
            return RespBDD.ERROR_GET
    else:
        return RespBDD.ERROR_CON

# Tareer todos los alumno que peretenecen a un grupo en especifico
def getAlumnosByGrupo(grupo):
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            cursor = conn.cursor()
            query = """
                select R1.nombre, R1.apellidoPa, R1.apellidoMa, R2.numBoleta from Usuario as R1, (
                    select * from Alumno where numBoleta in (
                        select numBoleta from Grupo_Alumno where nombreGrupo = '{}'
                    )
                ) as R2 where R1.idUsuario = R2.idUsuario;
            """.format(grupo.getGrupo())
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            return rows
        except expression as err:
            print("Error al cargar loa alumnos pro grupo ",str(err))
            return RespBDD.ERROR_GET
    else:
        return RespBDD.ERROR_CON

# Traer todas las evaluaciones de un alumno egun su numero de boleta
def getEvaluaciones(boleta):
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            cursor = conn.cursor()
            query = """
                SELECT fechaAplicacion, puntaje, moduloAprendizaje 
                FROM 'Evaluaciones' WHERE idEvaluacion in (
                    select idEvaluacion FROM 'Alumno_Evaluacion' 
                    WHERE numBoleta = '{}'
                )
            """.format(boleta)
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Error as err:
            print("Error al cargar las evaluaciones ", str(err))
            return RespBDD.ERROR_GET
    else:
        return RespBDD.ERROR_CON

# Traer toda la infromacion respecto a los grupos

def getFullDataGrupos():
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            cursor = conn.cursor()
            query = """
                select R1.nombreGrupo, R1.fechaCreacion, R2.cantidad
                from 'Grupo' as R1, (
                    select *,count(numBoleta) as cantidad 
                    from 'Grupo_Alumno' 
                    group by nombreGrupo
                ) as R2
                where R1.nombreGrupo = R2.nombreGrupo
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Error as err:
            print("Error al cargar los datos de full grupo", str(err))
            return RespBDD.ERROR_GET            
    else:
        return RespBDD.ERROR_CON


# Eliminar un usuario que es alumno de las base de datos
def eliminaAlumnobyBoleta(boleta):
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            cursor = conn.cursor()
            query = """
                delete from 'Usuario' WHERE ROWID in (
                    select idUsuario from 'Alumno' WHERE numBoleta = ?
                );
            """
            cursor.execute(query,(boleta,))
            conn.commit()                      
            print("Alumno eliminado")                     
            conn.close()
            return RespBDD.SUCCESS
        except Error as err:
            print("Error al eliminar un alumno ",str(err))
            return RespBDD.ERROR_ON_DELETE        
    else:
        return RespBDD.ERROR_CON

# Conseguir los datos del admisntrador
def getCredencialesAdmin():
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            cursor = conn.cursor()
            query = 'SELECT * FROM Profesor'
            cursor.execute(query)
            rows = cursor.fetchone()
            conn.close()
            return rows
        except Error as err:
            print("Error al tarer los datos del adminstrador ",str(err))
            return RespBDD.ERROR_GET
    else:
        return RespBDD.ERROR_CON


# Trae la cantidad de alumnos registrados en el sistema
def countAlumnosManager():
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            curosr = conn.cursor()
            query = """select count(*) from Alumno;"""
            curosr.execute(query)
            rows = curosr.fetchone()
            return rows
        except Error as err:
            print("Error al contar los alumnos ",str(err))
            return RespBDD.ERROR_GET
            pass
    else:
        return RespBDD.ERROR_CON

# Actualiza los datos de un estudiante
def actualizaAlumnoManager(alumno,grupo,oldBoleta):
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            cursor = conn.cursor()
            # Actualizar datos generales de usuario
            query = """
            update Usuario 
            set 
            nombre = ?,
            apellidoPa = ?,
            apellidoMa = ?
            where idUsuario in (
                select idUsuario 
                from Alumno 
                where numBoleta = ?
            )
            """
            # Ejecutamos consulta
            cursor.execute(query,(
                alumno.getNombre(),
                alumno.getApelldioPa(),
                alumno.getApellidoMa(),
                oldBoleta,
                )
            )
            # Guardamos cambios
            conn.commit()
            # Actualizamos boleta
            query="""
            update Alumno 
            set numBoleta = ? 
            where numBoleta = ?
            """
            cursor.execute(query,(
                alumno.getBoleta(),
                oldBoleta,
            ))
            # Guardamos cambios en la BDD
            conn.commit()

            # Actualizamos alumno en grupo
            query = """
            update Grupo_Alumno 
            set nombreGrupo = ? 
            where numBoleta = ?
            """
            # Ejecutamos consulta
            cursor.execute(query,(
                grupo.getGrupo(),
                alumno.getBoleta(),
            ))
            # Guardamos cambios
            conn.commit()
            # Cerramos conexión
            conn.close()
            return RespBDD.SUCCESS            
        except Error as err:
            print("Error al actualizar datos ",str(err))
            return RespBDD.ERROR_ON_UPDATE
    else:
        return RespBDD.ERROR_CON


# Contar el numero de grupos en el siatma
def countGruposManager():
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            cursor = conn.cursor()
            query = """select count(*) from Grupo"""
            cursor.execute(query)            
            rows = cursor.fetchone()
            conn.close()
            return rows
        except Error as err:
            print("Error al cargar el número de grupos ",str(err))
            return RespBDD.ERROR_GET
    else:
        return RespBDD.ERROR_CON

    
# Elimina datos de un grupo
def eliminaDatosGrupoManager(grupo,all_alu):
    conn = connectionDBManager()
    if not conn == RespBDD.ERROR_CON:
        try:
            cursor = conn.cursor()            
            query1 = """
            delete from Usuario where idUsuario in (
                select idUsuario from Alumno where numBoleta in (
                    select numBoleta from Grupo_Alumno WHERE nombreGrupo = ?
                )
            )
            """
            if all_alu:
                cursor.execute(query1,(grupo.getGrupo(),))
                conn.commit()                            
            else:
                query2 = """delete from Grupo where nombreGrupo = ?"""            
                cursor.execute(query2,(grupo.getGrupo(),))
                conn.commit()
                cursor.execute(query1,(grupo.getGrupo(),))                
                conn.commit()
            conn.close()
            return RespBDD.SUCCESS    
        except Error as err:
            print("Error al eliminar datos de grupo",str(err))
            return RespBDD.ERROR_ON_DELETE        
    else:
        return RespBDD.ERROR_CON

# Actualizar nombre de un grupo
def actualizaGrupoManager(grupo,new_name):
    conn = connectionDBManager()
    try:
        cursor = conn.cursor()            
        query = "update Grupo set nombreGrupo = ? where nombreGrupo = ?"
        cursor.execute(query,(new_name,grupo.getGrupo(),))
        conn.commit() 
        conn.close()                                   
        return RespBDD.SUCCESS    
    except Error as err:
        print("Error al actualizar nombre de grupo",str(err))
        return RespBDD.ERROR_ON_UPDATE       
    else:
        return RespBDD.ERROR_CON


# Actualiza los datos del adminstrador
def actualizaDatosAdminManager(profesor):
    conn = connectionDBManager()
    try:
        cursor = conn.cursor()            
        # Actualizar datos generales de usuario
        query = """
        update Usuario 
        set 
        nombre = ?,
        apellidoPa = ?,
        apellidoMa = ?
        where idUsuario in (
            select idUsuario 
            from Profesor            
        )
        """
        cursor.execute(query,
            (
                profesor.getNombre(),
                profesor.getApelldioPa(),
                profesor.getApellidoMa(),
            )
        )
        conn.commit() 

        # Actualizamos datos del admin
        query = """
        update Profesor set 
        userName = ?, 
        correo = ?        
        where idUsuario in (
            select idUsuario from Profesor
        )
        """
        cursor.execute(query,
            (
                profesor.getUserName(),
                profesor.getCorreo(),                
            )
        )
        conn.commit() 
        conn.close()                                   
        return RespBDD.SUCCESS    
    except Error as err:
        print("Error al actualizar datos del admin",str(err))
        return RespBDD.ERROR_ON_UPDATE       
    else:
        return RespBDD.ERROR_CON


# Actualiza password de administrador
def actualizaPasswordAdminManager(psd):
    conn = connectionDBManager()
    try:
        cursor = conn.cursor()                    
        # Actualizamos psd del admin
        query = """
        update Profesor set 
        password = ?               
        where idUsuario in (
            select idUsuario from Profesor
        )
        """
        cursor.execute(query,(psd,))
        conn.commit() 
        conn.close()                                   
        return RespBDD.SUCCESS    
    except Error as err:
        print("Error al actualizar password del admin",str(err))
        return RespBDD.ERROR_ON_UPDATE       
    else:
        return RespBDD.ERROR_CON


# consigue todos los datos genrales del Admin
def datosGeneralesAdminManager():
    conn = connectionDBManager()
    try:
        cursor = conn.cursor()                    
        # Actualizamos psd del admin
        query = """
        select R1.nombre, R1.apellidoPa, R1.apellidoMa, R2.userName, R2.correo 
        from Usuario as R1,Profesor as R2  where 
        R1.idUsuario in (
            select idUsuario from Profesor
        )
        """
        cursor.execute(query)
        rows = cursor.fetchone()   
        conn.close()                               
        return rows   
    except Error as err:
        print("Error al cargar datos del admin",str(err))
        return RespBDD.ERROR_GET       
    else:
        return RespBDD.ERROR_CON

# Cambia las credenciales del administrador
def updateCredentialsManager(new_psd,new_username):
    conn = connectionDBManager()
    try:
        cursor = conn.cursor()                    
        # Actualizamos psd del admin
        query = """
        update Profesor set 
        password = ?, username = ?               
        where idUsuario in (
            select idUsuario from Profesor
        )
        """
        cursor.execute(query,(new_psd,new_username,))
        conn.commit() 
        conn.close()                                   
        return RespBDD.SUCCESS   
    except Error as err:
        print("Error al actualizar datos del admin",str(err))
        return RespBDD.ERROR_ON_UPDATE       
    else:
        return RespBDD.ERROR_CON