using System;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;
using Acupunator.Models;
namespace Acupunator
{
    class DeserializeJsonData
    {
        static void Main(string[] args)
        {
            string data1 = getDataJson("c:/Users/Rodrigo García/Desktop/chanelsData.json");
            string data2 = getDataJson("...../shared/dataShared.json");
            //Deserializamos el JSON y obtenemos un obj deserializado (SÓLO EL CANL DEL PULMÓN)
            Chanel ObjjDeserialized = DeserializeData(data1); //Canales
            SharedData objShared = DeserializeDataShared(data2); //Obj comparitod por desktop app
            //Impimirmos algunos elementos del Obj canal 
            Console.WriteLine(string.Format("Canal:> {0} Punto 1:>  {1} Alias del punto 1:> {2}", 
                ObjjDeserialized.Name, ObjjDeserialized.Points[0].Name, ObjjDeserialized.Points[0].Alias));

            Console.WriteLine(string.Format("Tipo:> {0} Canal:> {1} Rol:> {2} NumBoleta:>{3}",objShared.Tipo, objShared.Canal,objShared.Rol, objShared.NumBoleta));                
        }

        /*
         * Éste método se encarga de parsear un arichivo JSON a una cadena de texto
        */
        public static string getDataJson(string path)
        {
            string data;
            using(var reader = new StreamReader(path))
            {
                data = reader.ReadToEnd();
            }

            return data;
        }
        /*
         * Este método deserializa una cadena de texto con formato JSON y lo mapea a clases previaente definidas
        */
        public static Chanel DeserializeData(string data)
        {            
            var dataDeserialized = JsonConvert.DeserializeObject<List<Chanel>>(data);
            return dataDeserialized[0]; //Canal del pulmón
        }

        public static SharedData DeserializeDataShared(string data){
            var dataDeserialized = JsonConvert.DeserializeObject<List<SharedData>>(data);
            return dataDeserialized[0]; //Obj compartido por desktop app        }
    }
}

