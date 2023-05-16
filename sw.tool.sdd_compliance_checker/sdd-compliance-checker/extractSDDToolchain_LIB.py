#! usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
# This is the Library file containing all functions for Select, Insert, Update, Delete Data From Database
# Usage :  Import SDD_csv_to_db_LIB
################################################################################
import pymssql
import sys
##############################################################################
# Function Name  : connect_to_mssql_db
# Arguments      : db_server_name, db_user_name, db_password, db_name
# Return Value   : 0,-1
# Called By      : main
# Description    : Function to Connect to MSSQl Database Server.
################################################################################
def connect_to_mssql_db(db_server_name, db_user_name, db_password, db_name):
    print(f"\nConnecting to Database -> {db_server_name}")

    try:
        server = pymssql.connect(db_server_name, db_user_name, db_password, db_name)
    except Exception as e:
        print(f"Exception Occurred: Problem in establishing database server connection: {e}")
        sys.exit(-1)
    else:
        print(f"Connected to Database {db_name} Successfully as {db_user_name}!") 
        return server

################################################################################
# Function Name  : get_table_info
# Arguments      : csv_row, table_name, cursor,condition
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is used to run Select Query for Data from particular Table.
################################################################################

def get_table_info(table_name, cursor, condition):
    data = []
    # print(f"SELECT * FROM {table_name} where {condition}")
    # Extracting Information From Table.
    cursor.execute(
        f"SELECT * FROM {table_name} where {condition}"
 
    )
    # Getting Data From Above Query.
    data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    if data:
        return data[-1]
    else:
        return data

################################################################################
# Function Name  : insert_table_info
# Arguments      : csv_row, server, table_name, cursor, db_columns, db_values
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is used to run Insert Query for Data from particular Table.
################################################################################
def insert_table_info(server, table_name, cursor, db_columns, db_values):
    cursor.execute(
        f"INSERT INTO {table_name}({db_columns}) VALUES ({db_values})"
    )
    server.commit()

# ################################################################################
# # Function Name  : update_table_info
# # Arguments      : csv_row, server, table_name, cursor, data, condition
# # Return Value   : 0,-1
# # Called By      : main
# # Description    : This function is used to run Update Query for Data from particular Table.
# ################################################################################
# def update_table_info(server, table_name, cursor, data, condition):
#     cursor.execute(
#         f"UPDATE {table_name} SET {data}  WHERE {condition}"
#     )
#     server.commit()

