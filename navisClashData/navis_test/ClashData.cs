using System;
using System.IO;
using System.Data;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Forms;


//Navisworks API references
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.DocumentParts;
using Autodesk.Navisworks.Api.Clash;
using Autodesk.Navisworks.Internal.ApiImplementation;
using Autodesk.Navisworks.Api.Automation;
using Autodesk.Navisworks.Api.Plugins;


namespace ClashData
{
    //plugin attributes require Name, DeveloperID and optional parameters
    [PluginAttribute("clash_sqlite_export", "Derek B", DisplayName = "Export Clashes to SQLite", ToolTip = "Exports clash data to XML them to sqlite database.", ExtendedToolTip = "Plugin Version 2022.1.0.2, EXE Version v1.0.2")]
    [AddInPluginAttribute(AddInLocation.AddIn, Icon = "C:\\Program Files\\Autodesk\\Navisworks Manage 2021\\Plugins\\clash_sql_export\\resources\\16x16_sqlite_export_img.bmp",
        LargeIcon = "C:\\Program Files\\Autodesk\\Navisworks Manage 2021\\Plugins\\clash_sqlite_export\\resources\\32x32_sql_export_img.bmp")]

    public class ClashData : AddInPlugin
    {
        public override int Execute(params string[] parameters)
        {
            Document document = Autodesk.Navisworks.Api.Application.ActiveDocument;
            DocumentClash documentClash = document.GetClash();
            var allTests_copy = documentClash.TestsData.CreateCopy();
            //DocumentModels docModel = document.Models;


            //-----------------------------------------------------------------------------------------
            //Check if Clash Test have even been created
            //If no clash tests created, exit program
            int check = allTests_copy.Tests.Count;
            if (check == 0)
            {
                MessageBox.Show("No clash tests currently exist!");
            }
            //-----------------------------------------------------------------------------------------


            ////Create data table to stor clash status counts
            //DataTable dt_test_data = new DataTable("Test results by Status");
            //dt_test_data.Columns.Add(new DataColumn("Test", typeof(System.String)));
            //dt_test_data.Columns.Add(new DataColumn("New", typeof(System.Int32)));
            //dt_test_data.Columns.Add(new DataColumn("Active", typeof(System.Int32)));
            //dt_test_data.Columns.Add(new DataColumn("Reviewed", typeof(System.Int32)));
            //dt_test_data.Columns.Add(new DataColumn("Approved", typeof(System.Int32)));
            //dt_test_data.Columns.Add(new DataColumn("Resolved", typeof(System.Int32)));

            //------------------------------------------------------------------------------------------

            //This location will produce one xml that contains all clashes for a model.-------------------
            //Data set to store data tables
            //DataSet ds = new DataSet();

            //Get save folder-----------------------------------------------------
            FolderBrowserDialog fbd = new FolderBrowserDialog();
            fbd.Description = "Select folder where the clash data (XML) files will be saved";
            string sSelectedPath = "";
            if (fbd.ShowDialog() == DialogResult.OK)
            {
                sSelectedPath = fbd.SelectedPath;
            }

            //date to append for tile names------------------------------------------------------------
            string export_date = DateTime.Now.ToString("yyyy.MM.dd");

            //Store clash data in data table--------------------------------------
            foreach (ClashTest test in allTests_copy.Tests)
            {
                //This location will produce one xml per test.----------------------------------------
                //Data set to store data tables
                DataSet ds = new DataSet();

                //test id an name seperated-----------------------------------------------------------
                string testFullName = test.DisplayName.ToString();
                string testId = testFullName.Substring(0, 5);
                //MessageBox.Show(testId);
                string testName = testFullName.Substring(6);
                //MessageBox.Show(testName);

                //----------------------------------------------------------------------------------

                if (test.LastRun != null)
                {
                    //Create data table to stor clash data--------------------------------------------
                    DataTable dt_test_data = new DataTable("clash_result"); //old entry: test.DisplayName.ToString()
                    dt_test_data.Columns.Add(new DataColumn("test_id", typeof(System.String)));
                    dt_test_data.Columns.Add(new DataColumn("test_name", typeof(System.String)));
                    dt_test_data.Columns.Add(new DataColumn("clash_guid", typeof(System.String)));
                    dt_test_data.Columns.Add(new DataColumn("clash_id", typeof(System.String)));
                    dt_test_data.Columns.Add(new DataColumn("date_created", typeof(System.String)));
                    dt_test_data.Columns.Add(new DataColumn("group_name", typeof(System.String)));
                    dt_test_data.Columns.Add(new DataColumn("status", typeof(System.String)));
                    dt_test_data.Columns.Add(new DataColumn("element_1_guid", typeof(System.String)));
                    dt_test_data.Columns.Add(new DataColumn("element_2_guid", typeof(System.String)));
                    dt_test_data.Columns.Add(new DataColumn("export_date", typeof(System.String)));
                    dt_test_data.Columns.Add(new DataColumn("assigned_to", typeof(System.String)));


                    foreach (SavedItem issue in test.Children)
                    {
                        //Sort individual clashes------------------------------------------------------------
                        if (issue.IsGroup == false)
                        {
                            ClashResult clashResult = issue as ClashResult;

                            DateTime cTime = (DateTime)clashResult.CreatedTime;
                            String newTime = cTime.ToString("yyyy.MM.dd");

                            if (clashResult.Item1 != null && clashResult.Item2 != null)
                            {
                                dt_test_data.Rows.Add(testId, testName, clashResult.Guid, clashResult.DisplayName, newTime, "not_grouped", clashResult.Status, clashResult.Item1.InstanceGuid, clashResult.Item2.InstanceGuid, export_date, clashResult.AssignedTo);
                            }
                            if (clashResult.Item1 == null && clashResult.Item2 == null)
                            {
                                dt_test_data.Rows.Add(testId, testName, clashResult.Guid, clashResult.DisplayName, newTime, "not_grouped", clashResult.Status, "no_guid", "no_guid", export_date, clashResult.AssignedTo);
                            }
                            if (clashResult.Item1 != null && clashResult.Item2 == null)
                            {
                                dt_test_data.Rows.Add(testId, testName, clashResult.Guid, clashResult.DisplayName, newTime, "not_grouped", clashResult.Status, clashResult.Item1.InstanceGuid, "no_guid", export_date, clashResult.AssignedTo);
                            }
                            if (clashResult.Item1 == null && clashResult.Item2 != null)
                            {
                                dt_test_data.Rows.Add(testId, testName, clashResult.Guid, clashResult.DisplayName, newTime, "not_grouped", clashResult.Status, "no_guid", clashResult.Item2.InstanceGuid, export_date, clashResult.AssignedTo);
                            }

                            //dt_test_data.Rows.Add(testId, testName, clashResult.Guid, clashResult.DisplayName, newTime, "not_grouped", clashResult.Status, clashResult.Item1.InstanceGuid, clashResult.Item2.InstanceGuid, export_date);
                        }

                        //find a property
                        //clashResult.Items.PropertyCategories.FindPropertyByDisplayName("Item", "GUID") 


                        //sort clashes in groups-----------------------------------------------------------
                        if (issue.IsGroup)
                        {
                            var group_name = issue.DisplayName;

                            foreach (SavedItem groupedClashes in ((GroupItem)issue).Children)
                            {
                                ClashResult gclashResult = groupedClashes as ClashResult;
                                //var testing_param = groupedClashes.DisplayName;
                                //MessageBox.Show(testing_param);

                                DateTime cTime = (DateTime)gclashResult.CreatedTime;
                                String newTime = cTime.ToString("yyyy.MM.dd");

                                if (gclashResult.Item1 != null && gclashResult.Item2 != null)
                                {
                                    dt_test_data.Rows.Add(testId, testName, gclashResult.Guid, gclashResult.DisplayName, newTime, group_name, gclashResult.Status, gclashResult.Item1.InstanceGuid, gclashResult.Item2.InstanceGuid, export_date, gclashResult.AssignedTo);
                                }
                                if (gclashResult.Item1 == null && gclashResult.Item2 == null)
                                {
                                    dt_test_data.Rows.Add(testId, testName, gclashResult.Guid, gclashResult.DisplayName, newTime, group_name, gclashResult.Status, "no_guid", "no_guid", export_date, gclashResult.AssignedTo);
                                }
                                if (gclashResult.Item1 != null && gclashResult.Item2 == null)
                                {
                                    dt_test_data.Rows.Add(testId, testName, gclashResult.Guid, gclashResult.DisplayName, newTime, group_name, gclashResult.Status, gclashResult.Item1.InstanceGuid, "no_guid", export_date, gclashResult.AssignedTo);
                                }
                                if (gclashResult.Item1 == null && gclashResult.Item2 != null)
                                {
                                    dt_test_data.Rows.Add(testId, testName, gclashResult.Guid, gclashResult.DisplayName, newTime, group_name, gclashResult.Status, "no_guid", gclashResult.Item2.InstanceGuid, export_date, gclashResult.AssignedTo);
                                }

                                //dt_test_data.Rows.Add(testId, testName, gclashResult.Guid, gclashResult.DisplayName, newTime, group_name, gclashResult.Status, gclashResult.Item1.InstanceGuid, gclashResult.Item2.InstanceGuid, export_date);
                            }
                        }
                    }
                    dt_test_data.WriteXml(sSelectedPath + @"\" + testFullName + "_" + export_date + ".xml", XmlWriteMode.WriteSchema);

                    ////used to display test data tables in a date set
                    //ds.Tables.Add(dt_test_data);

                    //using (var f = new display_xml.dataForm())
                    //{
                    //    f.dataGridView1.DataSource = dt_test_data;
                    //    f.ShowDialog();
                    //}

                }

                //This produces one excel file per test-------------------------------------------------
                //String savePath = @"C:\Users\dbecher\Documents\testing\" + testFullName + "_" + export_date + ".xlsx";
                //String savePath = sSelectedPath + testFullName + "_" + export_date + ".xlsx";
                //excel_file.ExcelUtility.CreateExcel(ds, savePath);

                //This location will produce one xml per test------------------------------------------
                //ds.WriteXml(@"C:\Users\dbecher\Documents\testing\" + testFullName + "_" + export_date + ".xml");
                //ds.WriteXml(sSelectedPath + @"\" + testFullName + "_" + export_date + ".xml", XmlWriteMode.WriteSchema);

                

                //This location will produce one xml that contains all clashes for a model.-------------------
                //ds.WriteXml(@"C:\Users\dbecher\Documents\testing\" + "Clash_Test_Data_" + export_date + ".xml");
                //ds.WriteXml(@"C:\Users\dbecher\Documents\testing\" + "Clash_Test_Data_" + export_date + ".xml", XmlWriteMode.WriteSchema);

            }

            var d = new database_question.DBQuestion();
            d.ShowDialog();

            return 0;
        }
    }
}
