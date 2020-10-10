--------------------------------------------
--CREACION DEL ESQUEMA DE LA BASE DE DATOS--
--------------------------------------------

CREATE TABLE `Usuario` (
	`idUsuario`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`nombre`	VARCHAR ( 30 ) NOT NULL,
	`apellidoPa`	VARCHAR ( 30 ) NOT NULL,
	`apellidoMa`	VARCHAR ( 30 ) NOT NULL
);


CREATE TABLE `Alumno` (
	numBoleta	VARCHAR ( 10 ) NOT NULL UNIQUE,
	idUsuario	INT NOT NULL UNIQUE,
    CONSTRAINT fk_idUsuario
	FOREIGN KEY(idUsuario) 
    REFERENCES Usuario(idUsuario) 
    ON DELETE CASCADE ON UPDATE CASCADE
	PRIMARY KEY(numBoleta)
);


CREATE TABLE `Profesor` (
	`userName`	VARCHAR ( 20 ) NOT NULL UNIQUE,
	`password`	BLOB NOT NULL,
	`correo`	VARHAR ( 40 ),
	`idUsuario`	INT NOT NULL UNIQUE,
	PRIMARY KEY(`userName`),
	FOREIGN KEY(`idUsuario`) REFERENCES `Usuario`(`idUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE `Grupo` (
	`nombreGrupo`	VARCHAR ( 30 ) NOT NULL UNIQUE,
    `fechaCreacion`	DATE NOT NULL,
    PRIMARY KEY(`nombreGrupo`)
);


CREATE TABLE `Evaluaciones` (
	`idEvaluacion`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`puntaje`	DOUBLE NOT NULL,
	`fechaAplicacion`	DATE NOT NULL,
	`moduloAprendizaje`	VARCHAR ( 45 ) NOT NULL
);


CREATE TABLE `Grupo_Alumno` (
	`nombreGrupo`	VARCHAR ( 30 ) NOT NULL,
	`numBoleta`	VARCHAR ( 10 ) NOT NULL UNIQUE,
	FOREIGN KEY(`numBoleta`) REFERENCES `Alumno`(`numBoleta`) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(`numBoleta`),
	FOREIGN KEY(`nombreGrupo`) REFERENCES `Grupo`(`nombreGrupo`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `Alumno_Evaluacion` (
	`idEvaluacion`	INT NOT NULL UNIQUE,
	`numBoleta`	VARCHAR ( 10 ) NOT NULL,
	FOREIGN KEY(`idEvaluacion`) REFERENCES `Evaluaciones`(`idEvaluacion`) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(`idEvaluacion`),
	FOREIGN KEY(`numBoleta`) REFERENCES `Alumno`(`numBoleta`) ON DELETE CASCADE ON UPDATE CASCADE
);

-----------------------
-- POBLAR BASE DE DATOS
-----------------------

/*
    Inserción de datos en tabla Usuario
*/
INSERT INTO Usuario VALUES(1,'Rodrigo','Garcia','Avila');
INSERT INTO Usuario VALUES(2,'Alexis','Ramos','Miranda');
INSERT INTO Usuario VALUES(3,'Samger','Linares','Risco');
INSERT INTO Usuario VALUES(4,'Arely','Osauna','Banda');
INSERT INTO Usuario VALUES(5,'Arturo','Ramos','Carlin');

insert into Usuario (nombre,apellidoPa,apellidoMa) values('Been','Amanda','Ger');

/*
    Inserción de datos en tabla Alumno
*/

INSERT INTO Alumno VALUES('2015350276',1);
INSERT INTO Alumno VALUES('2015350275',2);
INSERT INTO Alumno VALUES('2015350274',3);
INSERT INTO Alumno VALUES('2015350273',4);


/*
    Insertar a un usuario que es alumno con sus datos de usuario
    y ademas su número de boleta
*/

INSERT INTO Usuario VALUES(6,'Amanda','Ramos','Linares');
INSERT INTO Alumno VALUES('2015350270',last_insert_rowid());

/*
    Inserción de datos en tabla Profesor
*/
INSERT INTO Profesor VALUES('@gara',1010101,'correo123@correo.com',5);

/*
    Insertar a un usuario que es profesor con sus datos de usuario
    y ademas su correo, contraseña, y nombre de usuairo

    last_insert_rowid : devuelve el id del ultimo registro realizado
*/
INSERT INTO Usuario VALUES(7,'Carlin','Ramos','Linares');
INSERT INTO Profesor VALUES('@gara',1010101,5,'correo123@correo.com',last_insert_rowid());

/*
    Inserción de datos en tabla Grupo
*/
INSERT INTO Grupo VALUES('3CM3','2014-23-02');

/*
    Inserción de datos en tabla Grupo_Alumno
*/

INSERT INTO Grupo_Alumno VALUES('3CM3','2015350276');
INSERT INTO Grupo_Alumno VALUES('3CM3','2015350274');
INSERT INTO Grupo_Alumno VALUES('3CM3','2015350275');
INSERT INTO Grupo_Alumno VALUES('3CM4','2015350273');

/*
    Inserción de datos en tabla Evaluaciones
*/

INSERT INTO Evaluaciones VALUES(1,10,'20-05-11','Canal del brazo');
INSERT INTO Evaluaciones VALUES(2,5,'20-05-11','Canal del pecho');
INSERT INTO Evaluaciones VALUES(3,10,'20-05-11','Canal del brazo');
INSERT INTO Evaluaciones VALUES(4,6,'20-05-11','Canal del corazon');


/*
    Inserción de datos en tabla Evaluación
*/

INSERT INTO Alumno_Evaluacion VALUES(1,'2015350276');
INSERT INTO Alumno_Evaluacion VALUES(2,'2015350276');
INSERT INTO Alumno_Evaluacion VALUES(3,'2015350276');
INSERT INTO Alumno_Evaluacion VALUES(4,'2015350274');


-------------------------------------------
-- PRUEBAS DE FALLOS DE LA BASE DE DATOS---
-------------------------------------------


/*
    Tabla Usuario
    La tabla de usuario se identifica mediante su clave primaria 
    autoincrementable, no puede repetirse.
    La insersicion del siguente usuario debe fallar por existencia de llave en 
    la tabla

*/

INSERT INTO Usuario VALUES(5,'Armando','Jimenez','Hernandez');

/*
    Tabla Alumno
    La tabla de alumno se identificia mediante su clave primaria que es numBoleta,
    no puede repetirse.
    La insersicion del siguente usuario debe fallar por existencia de llave en 
    la tabla.
*/

INSERT INTO Alumno VALUES('2015350276',1);

/*
    Tabla Alumno
    La tabla de alumno se identificia mediante su clave primaria que es numBoleta,
    no puede repetirse y su llave foranea referente a la tabla usuario, por ende 
    debe existir un usuario con un id para poder registrse como tipo alumno
    La insersicion del siguente usuario debe fallar por inexistencia de usuario en 
    la tabla Usuario
*/

INSERT INTO Alumno VALUES('2015350123',200);



--------------
-- CONSULTAS--
--------------

/*
    Traer a todos los usuarios que son alumnos
    por nombre, apellido paterno, materno y boleta que son 
    de un grupo en específico 
    
*/

select R1.nombre, R1.apellidoPa, R1.apellidoMa, R2.numBoleta 
from Usuario as R1, (
	select * from Alumno where numBoleta in (
        select numBoleta 
        from Grupo_Alumno 
        where nombreGrupo = '3CM4'
    )
) as R2 where R1.idUsuario = R2.idUsuario;


/*
    Eliminar a un usuario que es alumno basado en su numero de boleta
*/

delete from Usuario where idUsuario in (
    select idUsuario from Alumno where numBoleta = '2015350276'
);



/*
    traer todos los datos de todos los grupos con la cantidad 
    de alumnos inscriptos en él
*/

select R1.nombreGrupo, R2.cantidad, R1.fechaCreacion
from 'Grupo' as R1, (
	select *,count(numBoleta) as cantidad 
	from 'Grupo_Alumno' 
	group by nombreGrupo
) as R2
where R1.nombreGrupo = R2.nombreGrupo;

/*
    Eliminar a un usuario que es profesor basado en su nombre de usuario
*/

delete from Usuario where idUsuario in (
    select idUsuario from Profesor where userName = '@gara'
);

/*
    Traer el total de usuarios que son alumnos de un grupo en especifico
*/

select count(*) from Alumno where numBoleta in (
	select numBoleta from Grupo_Alumno where nombreGrupo = '3CM3'
);

/*
    Traer el total de usuarios que son alumnos registrados en el sistema
*/

select count(*) from Alumno;

/*
    Traer el total de grupos  registrados en el sistema
*/

select count(*) from Grupo;


/*
    Traer nombre de usuario, apellido paterno, materno además de
    nombre de usuario del Profesor.
*/

select R1.nombre, R1.apellidoPa, R1.apellidoMa, R2.userName 
from Usuario as R1,Profesor as R2  where 
R1.idUsuario in (
	select idUsuario from Profesor where userName = '@gara'
);


/*
    Traer a todos los usuarios que son alumnos
    por nombre, apellido paterno, materno, número de boleta 
    y grupo al que pertenecen    
*/

select R3.nombre ||' ' || R3.apellidoPa || ' ' || R3.apellidoMa, R1.nombreGrupo, R1.numBoleta
from Grupo_Alumno as R1, Alumno as R2, Usuario as R3 
where R3.idUsuario = R2.idUsuario and R2.numBoleta = R1.numBoleta;

/*
    Eliminar todos los usuario alumnos de un grupo en especifico
*/

delete from Grupo_Alumno where nombreGrupo = '3CM3';



/*
    Traer todas laas calificiaciones de un aumno segun su numero
    de boleta
*/

SELECT fechaAplicacion, puntaje, moduloAprendizaje 
FROM 'Evaluaciones' WHERE idEvaluacion in (
	select idEvaluacion FROM 'Alumno_Evaluacion' 
    WHERE numBoleta = '2015350274'
);


/*

    Acutalizar datos del admisntrador, como:
        userName
        password
        correo
*/
update Profesor set userName = '@nuevoUser' where userName = '@actualUser';
update Profesor set password = 'nuevoPassword' where userName = '@actualUser';
update Profesor set correo = '@nuevoCorreo' where userName = '@actualUser';


/*
    TODO

    Realizar inserciones de relacion.
    Que no haya inserciones simultaneas 
    mientras se este realizando una accion podria modificar el útimo ID


    Antes de insertar cualquier usuario verificar desde el front primero
     lo siguiente:

        Si se desea insertar un alumno:
        Revisar en la base de datos para verificar si no hay un N°Bolta igual

        Si se desea insertar un profesor:
        Revisar en la base de datos si no hay un profesor con el mismo userName

        De ser vacia la consulta proceder al registrar
        Nombre de suaurio
        Datos de rol de usuario.

        

*/
