using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.Sql;
using Microsoft.Data.Sqlite;
//using System.Data.Sqlite;
using System.Diagnostics;
using System.Windows;
using System.Windows.Forms;

namespace fill_in_db
{
    public class FillDB
    {
        public static void Main_P()
        {
            try
            {
                string exe_path = @"C:\Program Files\Autodesk\IPS Navis clashes to database\clashes_to_sqlite_v1.0.2.exe";
                Process.Start(exe_path);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error accessing clashes exe file", ex.Message);
            }
        }

        public static void Main_C()
        {
            //future code to eliminate the need for the python exe file
        }

    }
}
