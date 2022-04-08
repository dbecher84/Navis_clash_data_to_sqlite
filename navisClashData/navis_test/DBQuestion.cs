using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace database_question
{
    public partial class DBQuestion : Form
    {
        public DBQuestion()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            fill_in_db.FillDB.Main_P();
            MessageBox.Show("XML data writing to database. Calling clashes_to_sql exe file");
        }

        private void button2_Click(object sender, EventArgs e)
        {
            MessageBox.Show("XML files have been created but no data has been written to the clash database");
        }
    }
}
