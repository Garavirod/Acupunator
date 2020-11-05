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
            //Console.WriteLine(data);
            DeserializeData(data);
            
        }

        public static string getDataJson()
        {
            string data;
            using(var reader = new StreamReader("c:/Users/Rodrigo García/Desktop/chanelsData.json"))
            {
                data = reader.ReadToEnd();
            }

            return data;
        }

        private static void DeserializeData(string data)
        {
            
            var dataDeserialized = JsonConvert.DeserializeObject<List<Chanel>>(data);
            Console.WriteLine(string.Format("Canal {0} punto 1 {1}", dataDeserialized[0].Name, dataDeserialized[0].Points[0].Name));
        }
    }
}

