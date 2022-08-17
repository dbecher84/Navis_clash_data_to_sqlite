

import datetime
import sqlite3
import easygui
import time
import sys
from sqlite3 import Error
#import xml.etree.ElementTree as ET

import read_xml_func

from fill_tables_func import fill_test_table
from fill_tables_func import fill_results_table
#from sqlite_create_db import create_clash_table
from choose_date_func import pick_date


#db_loc = "C:\\sqlite\\db\\navis_test_individ.db"
db_loc = easygui.fileopenbox(msg='Select Database to update.', title='Select Database file.', default='\\ipsdb.cor\prod\Projects')
#path='C:\\Users\\Derek.Becher\\Desktop\\test\\clashes_in_sql\\00.01 Structural vs Architectural.xml'
path = easygui.diropenbox(msg='Select folder containing clash results.', title='Select Test Folder', default='db_loc')

clash_list = []

clash_date_list = []


#connection to database
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        #print(e)
        easygui.msgbox(msg=e, title='Error Connecting to Database', ok_button='End')
 
    return conn


tests = [('00.00', 'Structural vs Structural'), ('00.01', 'Structural vs Architectural'), ('00.02', 'Structural vs Equipment'), ('00.03', 'Structural vs Process Piping'),
         ('00.04', 'Structural vs HVAC'), ('00.05', 'Structural vs Mechanical Piping'), ('00.06', 'Structural vs Fire Protection'), ('00.07', 'Structural vs Plumbing'), ('00.08', 'Structural vs Electrical'),
         ('01.02', 'Architectural vs Equipment'), ('01.03', 'Architectural vs Process Piping'),('01.04', 'Architectural vs HVAC'), ('01.05', 'Architectural vs Mechanical Piping'),
         ('01.06', 'Architectural vs Fire Protection'), ('01.07', 'Architectural vs Plumbing'), ('01.08', 'Architectural vs Electrical'), ('02.02', 'Equipment vs Equipment'),
         ('02.03', 'Equipment vs Process Piping'), ('02.04', 'Equipment vs HVAC'), ('02.05', 'Equipment vs Mechanical Piping'), ('02.06', 'Equipment vs Fire Protection'),
         ('02.07', 'Equipment vs Plumbing'),('02.08', 'Equipment vs Electrical'),
         ('03.03', 'Process Piping vs Process Piping'), ('03.04', 'Process Piping vs HVAC'), ('03.05', 'Process Piping vs Mechanical Piping'), ('03.06', 'Process Piping vs Fire Protection'),
         ('03.07', 'Process Piping vs Plumbing'), ('03.08', 'Process Piping vs Electrical'),
         ('04.04', 'HVAC vs HVAC'), ('04.05', 'HVAC vs Mechanical Piping'), ('04.06', 'HVAC vs Fire Protection'), ('04.07', 'HVAC vs Plumbing'), ('04.08', 'HVAC vs Electrical'),
         ('05.05', 'Mechanical Piping vs Mechanical Piping'), ('05.06', 'Mechanical Piping vs Fire Protection'), ('05.07', 'Mechanical Piping vs Plumbing'), ('05.08', 'Mechanical Piping vs Electrical'),
         ('06.06', 'Fire Protection vs Fire Protection'), ('06.07', 'Fire Protection vs Plumbing'), ('06.08', 'Fire Protection vs Electrical'),
         ('07.07', 'Plumbing vs Plumbing'), ('07.08', 'Plumbing vs Electrical'),
         ('08.08', 'Electrical vs Electrical'), ('99.99', 'Verity Clash Results')]

#tests = [('00.00', 'Clash Test 1'), ('00.01', 'Clash Test 2'), ('00.02', 'Clash Test 3')]

#populate clash test table
def test_table():
    '''populate table with tests name & id'''
    #create a database connection
    conn = create_connection(db_loc)
    with conn:
        # create a new project
        for item in tests:
            project = (item);
            project_id = fill_test_table(conn, project)
    conn.close()



def clash_table():
    '''populate results table'''
    #create a database connection
    conn = create_connection(db_loc)
    with conn:
        # create a new project
        i = 0
        for item in clash_list:
            #print (item)
            clash = (item);
            clash_id = fill_results_table(conn, clash)
            i =+ 1
            
    conn.close()
    

#def table_name_add_date():
#    '''adds date to end of new table named clash_results'''
#    now = datetime.datetime.now()
#    now2 = now.strftime('%Y_%m_%d')

#    conn = create_connection(db_loc)
    
#    rename_table = "ALTER TABLE clash_results RENAME TO newname"
#    new_name = rename_table.replace('newname', 'clash_results_' + str(now2))
#    cursor = conn.cursor()
#    cursor.execute(new_name)
#    conn.close


        
def get_tests(date):
    files_not_found = []
    for item in tests:
        file_path = path + '\\' + item[0] + ' ' + item[1] + '_' + date + '.xml'
        file_name = item[0] + ' ' + item[1] + ' ' + '.xml'
        try:
            read_xml_func.read_tests(item[0], file_path)
        except FileNotFoundError:
            #print ('File Not Found:' + file_path + '\n'
                   #'If clash test has never been ran no XML file will be produced.')
            files_not_found.append(file_name)
        except Exception as e:
            error_string = 'Unexpected error:' + str(e)
            easygui.msgbox(msg=error_string, title='Error Getting Test Files', ok_button='End')
            
    #print ('These files were not found:')

    easy_display_list = ''
    for item in files_not_found:
        #print (item)
        easy_display_list += '\n' + item
    easygui.msgbox(msg=easy_display_list, title='Files not found', ok_button='Continue')
        
    #unpause_by_user = input('Press enter to continue')

if __name__ == '__main__':
    #user_date_input = easygui.enterbox(msg='Is the test date todays date? Enter Y or N.', title='Date of test Export')
    user_date_input = easygui.ynbox(msg='Is the test date todays date?', choices=('[<F1>]Yes', '[<F2>]No'), default_choice='[<F1>]Yes')
    date_count = 0
    results_date = pick_date(user_date_input, date_count)
    if results_date == 'None' and date_count < 3:
        while date_count < 3 and results_date == 'None':
            date_count += 1
            results_date = pick_date(user_date_input, date_count)

    if results_date =='None' and date_count == 3:
        easygui.msgbox(msg='To many wrong date enteries. Program Ending.', title='Results', ok_button='End')
        sys.exit()
        
    easygui.msgbox(msg=results_date, title='Date Entered', ok_button='Continue')
    
    get_tests(results_date)

 
    clash_list = read_xml_func.clash_list
    #print (len(clash_list))
    test_list = []
    for item in clash_list:
       if len(item) != 9:
            test_list.append(item)
    #print (test_list)
    

    #user_input_pop_tests = easygui.enterbox(msg='Has the test table already been populated? Y or N.', title='Populate Test Table in Database')
    user_input_pop_tests = easygui.ynbox(msg='Has the test table already been populated?', choices=('[<F1>]Yes', '[<F2>]No'), default_choice='[<F1>]Yes')
    if user_input_pop_tests == True:
        try:
            clash_table()
            easygui.msgbox(msg='Results data added successfully.', title='Results', ok_button='Continue')
        except Exception as e:
            error_string = 'Unexpected error:' + str(e)
            easygui.msgbox(msg=error_string, title='Results', ok_button='End')
            
    elif user_input_pop_tests == False:
        try:
            test_table()
            clash_table()
            easygui.msgbox(msg='Results data added successfully.', title='Results', ok_button='Continue')
        except Exception as e:
            e_string = str(e)
            if e_string == 'UNIQUE constraint failed: clash_test.id':
                error_string = 'Error writing to clash tests table-' + str(e) + ': ' + 'Clash Test table may have been populate previously. Will attempt to populate clash results table.'
                easygui.msgbox(msg=error_string, title='Results', ok_button='OK')
            else:
                error_string = 'Unknown error writing to clash test table-' + str(e) + ': ' + 'Will attempt to populate clash results table.'
                easygui.msgbox(msg=error_string, title='Results', ok_button='OK')
            try:
                clash_table()
                easygui.msgbox(msg='Clashes test results were successfully added', title='Results', ok_button='OK')
            except:
                easygui.msgbox(msg='Clashes test results also failed to populate database', title='Results', ok_button='End')
    else:
        easygui.msgbox(msg='Invalid Input received from populate test table dialog. The program will now end', title='Input Error', ok_button='End')

