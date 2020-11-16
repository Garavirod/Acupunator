using System;
using System.Collections.Generic;
using System.Text;

namespace Acupunator.Models
{
    public class Point
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Alias { get; set; }
        public string Location { get; set; }
        public string Function { get; set; }
        public string Directions { get; set; }
        public string Puncture { get; set; }
        public string[] Combinations { get; set; }
        public string Remark { get; set; }
    }
}
