using System;
using System.Collections.Generic;
using System.Text;
using System.Data.SQLite; //Instalar dep

namespace Acupunator.Models //esta en la misma carpta de modelos (Point, Channel, sharedData)
{
    public class RegisterDBScore
    {
        public void asignScore(SharedData app)
        {
            if (app.Tipo.Equals("Evaluación") && app.Rol.Equals("Alumno"))
            {
                //path del archivo file.db
                string pathbd = @"URI=file:C:/Users/Rodrigo García/Desktop/AcupunatorDB.db";
                using var conn = new SQLiteConnection(pathbd);
                //Abrimos conexión con la base de datos
                conn.Open();
                using var cmd = new SQLiteCommand(conn);

                //INSERTAMOS EVALUACIÓN

                //Cargamos el string de la query
                cmd.CommandText = "INSERT INTO Evaluaciones(puntaje,fechaAplicacion,moduloAprendizaje) VALUES(@puntaje,@fecha,@modulo)";                
                //Agregamos los valores a los parámetros de la query
                cmd.Parameters.AddWithValue("@puntaje", app.Cal);
                cmd.Parameters.AddWithValue("@fecha", DateTime.Now.ToString("yyyy-MM-dd"));
                cmd.Parameters.AddWithValue("@modulo", app.Canal);
                //Preparamos la consulta
                cmd.Prepare();
                //Ejecutamos la consulta
                cmd.ExecuteNonQuery();

                //INSERTAMOS ALUMNOS EVALUACIÓN                
                cmd.CommandText = "INSERT INTO Alumno_Evaluacion(idEvaluacion,numBoleta) VALUES(last_insert_rowid(),@numBoleta)";                
                cmd.Parameters.AddWithValue("@numBoleta", app.NumBoleta);
                //Preparamos la consulta
                cmd.Prepare();
                //Ejecutamos la consulta
                cmd.ExecuteNonQuery();

                Console.WriteLine("Score was inserted!!");
            }         
        }

    }
}
