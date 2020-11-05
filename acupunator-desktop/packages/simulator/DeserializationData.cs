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
            string data = getDataJson();
            //Deserializamos el JSON y obtenemos un obj deserializado (SÓLO EL CANL DEL PULMÓN)
            Chanel ObjjDeserialized = DeserializeData(data); 
            //Impimirmos algunos elementos del Obj canal 
            Console.WriteLine(string.Format("Canal:> {0} Punto 1:>  {1} Alias del punto 1:> {2}", 
                ObjjDeserialized.Name, ObjjDeserialized.Points[0].Name, ObjjDeserialized.Points[0].Alias));
        }

        /*
         * Éste método se encarga de parsear un arichivo JSON a una cadena de texto
        */
        public static string getDataJson()
        {
            string data;
            using(var reader = new StreamReader("c:/Users/Rodrigo García/Desktop/chanelsData.json"))
            {
                data = reader.ReadToEnd();
            }

            return data;
        }
        /*
         * Este método deserializa una cadena de texto con formato JSON y lo mapea a clases previaente definidas
        */
        private static Chanel DeserializeData(string data)
        {            
            var dataDeserialized = JsonConvert.DeserializeObject<List<Chanel>>(data);
            return dataDeserialized[0]; //Canal del pulmón
        }
    }
}

