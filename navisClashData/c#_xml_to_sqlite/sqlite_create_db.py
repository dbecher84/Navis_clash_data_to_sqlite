
###create databse file and sets up tables###

import easygui
import sqlite3
import os
from sqlite3 import Error
from sys import exit
 
#db_location = "C:\\sqlite\\db\\navis_test_individ.db"

f_loc = easygui.diropenbox(msg='Select Folder for Database File.', title='Select Database Folder', default='C:\\')
if f_loc == None:
    print ('No folder was selected. The program will now terminate.')
    exit()
    
db_name_user_input = input('Enter name of Database File. ')
db_name = db_name_user_input.replace(' ', '_')

if db_name_user_input:
    db_location = f_loc + '\\' + db_name + '.db'
    print (db_location)
else:
    print ('No Database file name was entered. A temporary name will be used. ')
    db_location = f_loc + '\\' + 'his_name_needs_to_be_changed_before_power_bi_linking.db'


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_location)
        print(sqlite3.version)
    except Error as e:
        print(e)


#create tables in database
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


#main program to create tables
def create_test_table():
    #database = r"C:\\sqlite\\db\\navis_test.db"
 
    sql_create_clash_test_table = """ CREATE TABLE IF NOT EXISTS clash_test  (
                                        id text PRIMARY KEY,
                                        name text NOT NULL
                                    ); """


    # create a database connection
    conn = sqlite3.connect(db_location)
 
    # create tables
    if conn is not None:
        create_table(conn, sql_create_clash_test_table)
 
    else:
        print("Error! cannot create the database connection.")

    conn.close()
    

def create_clash_table():
    #database = r"C:\\sqlite\\db\\navis_test.db"

    sql_create_clash_results_table = """ CREATE TABLE IF NOT EXISTS clash_results (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        guid text NOT NULL,
                                        clash_id text NOT NULL,
                                        status text NOT NULL,
                                        element_id_1 text NOT NULL,
                                        element_id_2 text NOT NULL,
                                        parent_group text NOT NULL,
                                        created_date text NOT NULL,
                                        assigned_to text NOT NULL,
                                        test_date text NOT NULL,
                                        test_id text NOT NULL
                                    ); """

     # create a database connection
    conn = sqlite3.connect(db_location)

    if conn is not None:
        create_table(conn, sql_create_clash_results_table)

    else:
        print("Error! cannot create the database connection.")

    conn.close()

 
if __name__ == '__main__':
    create_test_table()
    create_clash_table()
