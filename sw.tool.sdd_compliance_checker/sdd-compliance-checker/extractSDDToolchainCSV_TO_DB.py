#! usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
# This script is used to store CI Information in the database
# Usage : python extractSDDToolchain_CSV_TO_DB.py
#          --db_user_name = <DB_USERNAME> --db_password = <DB_PASSWORD> --input_csv_file = ".csv"
# Based on different scenario script will return different exit code as follows:
#  0: Data Inserted Successfully.
# -1: Script Failure.
################################################################################

# Required Libraries
import sys
import argparse
import csv
import extractSDDToolchainMetricsConfig as config
sys.path.append('../')
import extractSDDToolchain_LIB as lib

# Defining Global Parameters
db_server_name = config.db_server_name
db_user_name = ""
db_password = ""
input_csv_file = ""
db_name = config.db_name
db_map = config.csv_header
db_tables = config.db_Tables

################################################################################
# Function Name  : read_csv
# Arguments      : input_csv_file
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to read input CSV File.
################################################################################
def read_csv(input_csv_file):
    global db_map
    csv_Data = []
    print(f"\nReading CSV File : {input_csv_file}")
    
    if input_csv_file != "" and '.csv' in input_csv_file:            
        try:
            # Checking input csv in dictionary format for each row.
            with open(input_csv_file, 'r') as data:
                # Checking of all columns defined in database tables are present in CSV file
                for csv_header in csv.DictReader(data).fieldnames:
                    if csv_header in list(db_map.values()):
                        pass
                    else:
                        print(f"Exception Occurred: Column {csv_header} not found in CSV!")
                        sys.exit(-1)
            # Appending all rows as dictionary to csv_data list
            with open(input_csv_file, 'r') as data:
                for csv_row in csv.DictReader(data):
                    csv_Data.append(csv_row)
        except Exception as e:
            print(f"Exception Occurred: Invalid file given as input. {e}")    
            sys.exit(-1) 
        else:
            return (csv_Data)
    else:
        print(f"Error : Exception Occurred Invalid CSV file given as input.")    
        sys.exit(-1) 

################################################################################
# Function Name  : store_projects
# Arguments      : csv_row, server, db_table, cursor
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to store data in projects table.
################################################################################
def store_projects(csv_row, server, db_tables, cursor):
    # Checking if project_name is not blank in csv row.
    if csv_row[db_map['project_name']]:
        try:
            project_name =""
            # Getting the select condition for projects table from config file.
            select_condition =  f"[project_name] = '{csv_row[db_map['project_name']]}'"
            # Calling the Select Query function from Library file.
            table_info = lib.get_table_info (db_tables['project']['name'], cursor, select_condition)
            # Getting the project name from table_info
            if table_info:
                project_name = table_info.get('project_name')
            # Insert if project name is None.
            if project_name.strip() == "":
                # Getting the db_columns & db_values from config file for insert query.
                insert_db_columns = db_tables['project']['insert']['db_columns']
                insert_db_values =  (db_tables['project']['insert']['db_values']).format(**locals())
                # Calling the insert Function to store data
                lib.insert_table_info(server, db_tables['project']['name'], cursor, insert_db_columns, insert_db_values)
            else:
                # Do nothing if project name is already present in database
                pass
        except Exception as e:
            print(f"Error : Exception Occurred  In project Table Query: {e}")    
            sys.exit(-1) 
    else:
        pass

################################################################################
# Function Name  : get_project_id
# Arguments      : csv_row, db_table,cursor
# Return Value   : 0,-1,project_id
# Called By      : main
# Description    : This function is to get project id from project Table.
################################################################################
def get_project_id(csv_row, db_tables, cursor):
    global project_id
    # Checking if project_name is not blank in csv row.
    project_id ="NULL"
    if csv_row[db_map['project_name']]:
        try:
            # Getting the select condition for project table From config file.
            select_condition = f"[project_name] = '{csv_row[db_map['project_name']]}'"
            # Calling the Select Query function from Library file.
            project_id_table_info = lib.get_table_info (db_tables['project']['name'], cursor, select_condition)
            # Getting the project From table_info
            if project_id_table_info:
                project_id = project_id_table_info.get('project_id')
        except Exception as e:
            print(f"Error : Exception Occurred unable to get project id in function get_project_id: {e}")    
            sys.exit(-1)     
    else:
        #pass
        return(project_id)
    return (project_id)

################################################################################
# Function Name  : store_autosaar_variant
# Arguments      : csv_row, server, db_table, cursor,type_id
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to store data in variant table.
################################################################################
def store_autosaar_variant(csv_row, server, db_tables, cursor,project_id):
    # Checking if Variant is not blank in csv row.
    if csv_row[db_map['Variant']]:
        try:
            Variant = ""
            # Getting the select condition for autosaar_Variant table from config file.
            select_condition =  f"[Variant] = '{csv_row[db_map['Variant']]}' and [project_id]={project_id}"
            # Calling the select query function from library file.
            table_info = lib.get_table_info (db_tables['autosaar_variant']['name'], cursor, select_condition)
            # Getting the type from Variant
            if table_info:
                Variant = table_info.get('variant')
            # Insert if Variant is None.
            if Variant.strip() == "":
                # Getting the db_columns & db_values from config file for insert query.
                insert_db_columns = db_tables['autosaar_variant']['insert']['db_columns']
                insert_db_values = (db_tables['autosaar_variant']['insert']['db_values']).format(**locals())
                # Calling the insert function to store data
                lib.insert_table_info(server, db_tables['autosaar_variant']['name'], cursor, insert_db_columns, insert_db_values)
            else:
                # Do Nothing If Variant is already present in table
                pass
        except Exception as e:
            print(f"Error : Exception Occurred In Autosaar Variant Table Query:",{e})    
            sys.exit(-1)     
    else:
        pass


################################################################################
# Function Name  : get_autosaar_variant_id
# Arguments      : csv_row, db_table, cursor,type_id
# Return Value   : 0,-1,Variant
# Called By      : main
# Description    : This function is to get autosaar variant id form autosaar variant table.
################################################################################
def get_variant_id(csv_row,db_tables, cursor,project_id):
    variant_id = "NULL"
    # Checking if Variant is not blank in csv row.
    if csv_row[db_map['Variant']]:
        try:
            # Getting the select condition for  variant id table From config file.
            select_condition = f"[Variant] = '{csv_row[db_map['Variant']]}' and [project_id] = {project_id}"
            # Calling the Select Query function from Library file.
            variant_id_table_info = lib.get_table_info (db_tables['autosaar_variant']['name'], cursor, select_condition)
            # Getting the Variant from table_info
            if variant_id_table_info:
                variant_id = variant_id_table_info.get('variant_id')
        except Exception as e:
            print(f"Error : Exception Occurred Unable to variant id in function Variant_id_table_info: {e}")    
            sys.exit(-1)     
    else:
        # pass
        return(variant_id)
    return (variant_id)


################################################################################
# Function Name  : store_customers
# Arguments      : csv_row, server, db_table, cursor , variant_id, project_id
# Return Value   : -1
# Called By      : main
# Description    : This function is to store data in Customer table.
################################################################################
def store_customers(csv_row, server, db_tables, cursor,variant_id,project_id):
    # Checking if Customer is not blank in csv row.
    if csv_row[db_map['Customer']]:
        try:
            Customer = ""
            if(variant_id =="NULL"):
                # Getting the select condition for customer table from config file.
                select_condition = f"[customer]='{csv_row[db_map['Customer']]}' and [project_id]={project_id} and [variant_id] is NULL"
            else :
                select_condition = f"[customer]='{csv_row[db_map['Customer']]}' and [variant_id]={variant_id} and [project_id]={project_id}"
            # Calling the select query function from library file.
            table_info = lib.get_table_info (db_tables['customers']['name'], cursor, select_condition)
            # Getting the from customer
            if table_info:
                Customer = table_info.get('customer')
            # Insert if Variant is None.
            if Customer.strip() == "":
                # Getting the db_columns & db_values from config file for insert query.
                insert_db_columns = db_tables['customers']['insert']['db_columns']
                insert_db_values = (db_tables['customers']['insert']['db_values']).format(**locals())
                # Calling the insert function to store data
                lib.insert_table_info(server, db_tables['customers']['name'], cursor, insert_db_columns, insert_db_values)
            else:
                # Do Nothing If customer is already present in table
                pass
        except Exception as e:
            print(f"Error : Exception Occurred  In Customer Table Query:",{e})    
            sys.exit(-1)     
    else:
        pass
    
################################################################################
# Function Name  : get_customer_id
# Arguments      : csv_row,db_table, cursor,project_id,variant_id
# Return Value   : 0,-1,Variant
# Called By      : main
# Description    : This function is to get get customer id form sw customer table.
################################################################################
def get_customer_id(csv_row,db_table, cursor,project_id,variant_id):
    customer_id = "NULL"
    # Checking if Customer  is not blank in csv row.
    if csv_row[db_map['Customer']]:
        try:
            if(variant_id =="NULL"):
                # Getting the select condition for customer table from config file.
                # If variant id is NULL
                select_condition = f"[customer]='{csv_row[db_map['Customer']]}' and [project_id]={project_id} and [variant_id] is NULL"
            else :
                select_condition = f"[customer]='{csv_row[db_map['Customer']]}' and [variant_id]={variant_id} and [project_id]={project_id}"
            # Calling the Select Query function from Library file.
            # print("This is select condition for customer_id",select_condition)
            customer_id_table_info = lib.get_table_info (db_table['customers']['name'], cursor, select_condition)
            # Getting the Variant from table_info
            if customer_id_table_info:
                customer_id = customer_id_table_info.get('customer_id')
        except Exception as e:
            print(f"Error : Exception Occurred Unable to customer id in function customer_id: ",{e})    
            sys.exit(-1)     
    else:
        # pass
        return(customer_id)
    return (customer_id)

################################################################################
# Function Name  : types
# Arguments      : csv_row, server, db_table, cursor
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to store data in type table.
################################################################################
def store_types(csv_row, server, db_table, cursor,project_id):
    # Checking if type is not blank in csv row.
    if csv_row[db_map['type']]:
        try:
            type = ""
            # Getting the project id from projects Table for foreign key referencing
            projectTable_select_condition =  f"[type] = '{csv_row[db_map['type']]}'"
            projectTable_info = lib.get_table_info (db_table['types']['name'], cursor, projectTable_select_condition)
            if projectTable_info:
                project_id = projectTable_info.get('project_id')
            # Getting the select condition for types  table From config file.
            select_condition =  f"[type] = '{csv_row[db_map['type']]}' and [project_id]={project_id}"
            # Calling the Select Query function from Library file.
            table_info = lib.get_table_info (db_table['types']['name'], cursor, select_condition)
            # Getting the type from table_info
            if table_info:
                type = table_info.get('type')
            # Insert if type is none.
            if type.strip() == "":
                # Getting the db_columns & db_values from config file for insert query.
                insert_db_columns = db_table['types']['insert']['db_columns']
                insert_db_values = (db_table['types']['insert']['db_values']).format(**locals())
                # Calling the insert function to store data
                lib.insert_table_info(server, db_table['types']['name'], cursor, insert_db_columns, insert_db_values)
            else:
                # Do Nothing If type is already present in table
                pass
        except Exception as e:
            print("Error : Exception Occurred In Type Table Query: ",{e})    
            sys.exit(-1)     
    else:
        pass

################################################################################
# Function Name  : get_type_id
# Arguments      : csv_row, db_table, cursor
# Return Value   : 0,-1,type_id
# Called By      : main
# Description    : This function is to get type id from types Table.
################################################################################
def get_type_id(csv_row, db_table, cursor):
    # Checking if type is not blank in csv row.
    type_id = "NULL"
    if csv_row[db_map['type']]:
        try:
            # Getting the select condition for types table From config file.
            select_condition = f"[type] = '{csv_row[db_map['type']]}'"
            # Calling the Select Query function from Library file.
            type_id_table_info = lib.get_table_info (db_table['types']['name'], cursor, select_condition)
            # Getting the type From table_info
            if type_id_table_info:
                type_id = type_id_table_info.get('type_id')
        except Exception as e:
            print(f"Error : Exception Occurred Unable to get type id in function get_type: {e}")    
            sys.exit(-1)     
    else:
        # pass
        return(type_id)
    return (type_id)

################################################################################
# Function Name  : store_sw_components
# Arguments      : csv_row, server, db_tables, cursor,type_id,variant_id,customer_id
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to store data in sw components table.
################################################################################
def  store_sw_components(csv_row, server, db_tables, cursor,type_id,variant_id,customer_id):
    # Checking if sw_component is not blank in csv row.
    if csv_row[db_map['sw_component']]:
        try:
            sw_component = ""
            if(variant_id =="NULL"):
                # Getting the select condition for Customer table from config file.
                select_condition =  f"[sw_component] = '{csv_row[db_map['sw_component']]}' and [type_id]={type_id}  and [customer_id]={customer_id} and [variant_id] is NULL"
            else :
                select_condition =  f"[sw_component] = '{csv_row[db_map['sw_component']]}' and [type_id]={type_id} and [variant_id]={variant_id}  and [customer_id]={customer_id}"
            # Calling the select query function from library file.
            table_info = lib.get_table_info (db_tables['sw_components']['name'], cursor, select_condition)
            # Getting the type from sw_components
            if table_info:
                sw_component = table_info.get('sw_component')
            # Insert if type is None.
            if sw_component.strip() == "":
                # Getting the db_columns & db_values from config file for insert query.
                insert_db_columns = db_tables['sw_components']['insert']['db_columns']
                insert_db_values = (db_tables['sw_components']['insert']['db_values']).format(**locals())
                # Calling the insert function to store data
                lib.insert_table_info(server, db_tables['sw_components']['name'], cursor, insert_db_columns, insert_db_values)
            else:
                # Do Nothing If sw_component is already present in table
                pass
        except Exception as e:
            print("Error : Exception Occurred  In   sw components table query: ",{e})    
            sys.exit(-1)     
    else:
        pass

################################################################################
# Function Name  : get_sw_component_id
# Arguments      : csv_row, server, db_tables, cursor,type_id,variant_id,customer_id
# Return Value   : 0,-1,sw_component_id
# Called By      : main
# Description    : This function is to get sw components id form sw components table.
################################################################################
def  get_sw_components_id(csv_row, db_tables, cursor,type_id,variant_id,customer_id):
    sw_component_id = "NULL"
    # Checking if sw component is not blank in csv row.
    if csv_row[db_map['sw_component']]:
        try:
            if(variant_id =="NULL"):
                # Getting the select condition for Customer table from config file.
                select_condition =  f"[sw_component] = '{csv_row[db_map['sw_component']]}' and [type_id]={type_id}  and [customer_id]={customer_id} and [variant_id] is NULL"
            else :
                select_condition =  f"[sw_component] = '{csv_row[db_map['sw_component']]}' and [type_id]={type_id} and [variant_id]={variant_id}  and [customer_id]={customer_id}"
            # Calling the Select Query function from Library file.
            sw_components_id_table_info = lib.get_table_info (db_tables['sw_components']['name'], cursor, select_condition)

            # Getting the sw_component_id from table_info
            if sw_components_id_table_info:
                sw_component_id = sw_components_id_table_info.get('sw_component_id')
        except Exception as e:
            print(f"Error : Exception Occurred Unable to get type id in function sw_components: {e}")    
            sys.exit(-1)     
    else:
        # pass
        return(sw_component_id)
    return (sw_component_id)

################################################################################
# Function Name  : stored_dev_branches
# Arguments      : csv_row, server, db_tables, cursor,type_id,variant_id,customer_id
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to store data in dev_branches table.
################################################################################
def store_dev_branches(csv_row, server, db_tables, cursor,type_id,variant_id,customer_id):
    # Checking if dev branches is not blank in csv row.
    if csv_row[db_map['branch']]:
        try:
            branch = ""
            # Getting the select condition for dev_branches table From config file.
            if(variant_id =="NULL"):
                # Getting the select condition for Customer table from config file.
                select_condition =  f"  [type_id]={type_id}  and [customer_id]={customer_id} and [variant_id] is NULL"
            else :
                select_condition =  f"  [type_id]={type_id} and [variant_id]={variant_id}  and [customer_id]={customer_id}"
            # Calling the Select Query function from Library file.
            table_info = lib.get_table_info (db_tables['dev_branches']['name'], cursor, select_condition)
            # Getting the type From dev_branches
            if table_info:
                branch = table_info.get('branch')
            # Insert if dev_branches is Blank.
            if branch.strip() == "":
                # Getting the db_columns & db_values from config file for insert query.
                insert_db_columns = db_tables['dev_branches']['insert']['db_columns']
                insert_db_values = (db_tables['dev_branches']['insert']['db_values']).format(**locals())
                # Calling the insert Function to store data
                lib.insert_table_info(server, db_tables['dev_branches']['name'], cursor, insert_db_columns, insert_db_values)
            else:
                # Do nothing if branch is already present in table 
                pass
        except Exception as e:
            print(f"Error : Exception Occurred in branch table query: {e}")    
            sys.exit(-1)     
    else:
        pass

################################################################################
# Function Name  : get_dev_branches_id
# Arguments      : csv_row,db_table, cursor,type_id
# Return Value   : 0,-1,branch_id
# Called By      : main
# Description    : This function is to get branch id from dev branches table.
################################################################################
def get_dev_branch_id(csv_row,db_tables,cursor,type_id,variant_id,customer_id):
    branch_id = "NULL"
    # Checking if branch is not blank in csv row.
    if csv_row[db_map["branch"]]:
        try:
            # Getting the select condition for branch id table From config file.
            if(variant_id =="NULL"):
                # Getting the select condition for Customer table from config file.
                select_condition =  f"[branch] = '{csv_row[db_map['branch']]}' and [type_id]={type_id} and [variant_id] is NULL and [customer_id]={customer_id} "
            else :
                select_condition =  f"[branch] = '{csv_row[db_map['branch']]}' and [type_id]={type_id} and [variant_id]={variant_id}  and [customer_id]={customer_id}"
            # Calling the Select Query function from Library file.
            dev_branch_id_table_info = lib.get_table_info (db_tables['dev_branches']['name'], cursor, select_condition)
            # Getting the type From table_info
            if dev_branch_id_table_info:
                branch_id = dev_branch_id_table_info.get('branch_id')
        except Exception as e:
            print(f"Error : Exception Occurred Unable to get branch id in function branch: {e}")    
            sys.exit(-1)     
    else:
        return(branch_id)
    return (branch_id)

################################################################################
# Function Name  : store_versions
# Arguments      : csv_row, server, db_table, cursor , branch_id, sw_component_id
# Return Value   : -1
# Called By      : main
# Description    : This function is to store data in versions table.
################################################################################
def store_versions(csv_row, server, db_tables, cursor,branch_id,sw_component_id):
    # Checking if type  is not blank in csv row.
    if csv_row[db_map['type']]:
        try:
            sw_component_rel_version = ""
            sdd_type = f"'{csv_row[db_map['type']]}'"
            sdd_type=str(sdd_type)
            # Checking type Release or Development  
            if('Release' in sdd_type ):
                if(csv_row[db_map['sw_component_rel_version']]):
                    sw_component_rel_version = f"'{csv_row[db_map['sw_component_rel_version']]}'" 
            elif ('Development'in sdd_type):
                if(csv_row[db_map['branch_version']]):
                    sw_component_rel_version = f"'{csv_row[db_map['branch_version']]}'"
            # Getting the from versions table for foreign key referencing
            if(sw_component_rel_version):
                # Getting  select conditon according to type (Release or Development) 
                if('Release' in sdd_type):
                    versions_select_condition =  f"[version_number] = {sw_component_rel_version} and [sw_component_id]= {sw_component_id}"
                else:
                    versions_select_condition =  f"[version_number] = {sw_component_rel_version} and [branch_id]={branch_id} and [sw_component_id]= {sw_component_id}"
                version_Table_info = lib.get_table_info (db_tables['versions']['name'], cursor, versions_select_condition)
                if(version_Table_info==[]):
                    #Inserting Data
                    insert_db_columns = db_tables['versions']['insert']['db_columns']
                    insert_db_values = (db_tables['versions']['insert']['db_values']).format(**locals())
                    # Calling the insert Function to store data
                    lib.insert_table_info(server, db_tables['versions']['name'], cursor, insert_db_columns,insert_db_values)
        except Exception as e:
            print(f"Exception Occurred: Error in sw_component_rel_version table query: {e}")    
            sys.exit(-1)     
    else:
        print("Warning : type column is empty or type column not exist")
        
################################################################################
# Function Name  : get_version_id
# Arguments      : csv_row, db_table, cursor,branch_id,sw_component_id
# Return Value   : -1,version_id
# Called By      : main
# Description    : This function is to get version id from versions table.
################################################################################
def get_version_id(csv_row, db_tables, cursor,branch_id,sw_component_id):
    version_id = "NULL"
    # Checking if type is not blank in csv row.
    if csv_row[db_map['type']]:
        try:
            sw_component_rel_version = ""
            sdd_type =  f"'{csv_row[db_map['type']]}'"
            if('Release' in sdd_type ):
                if(csv_row[db_map['sw_component_rel_version']]):
                    sw_component_rel_version = f"'{csv_row[db_map['sw_component_rel_version']]}'"          
            elif ('Development'in sdd_type):
                if(csv_row[db_map['branch_version']]):
                    sw_component_rel_version = f"'{csv_row[db_map['branch_version']]}'"  
            # Getting the  From versions Table for foreign key referencing
            if(sw_component_rel_version):
                # Getting the select condition for versions id table From config file.
                if('Release' in sdd_type):
                    select_condition =  f"[version_number] = {sw_component_rel_version} and [sw_component_id]= {sw_component_id} "
                else:
                    select_condition =  f"[version_number] = {sw_component_rel_version} and [sw_component_id]= {sw_component_id} and [branch_id]={branch_id}"
                # Calling the Select Query function from Library file.
                version_id_table_info = lib.get_table_info (db_tables['versions']['name'], cursor, select_condition)
                # Getting the version id From version_id_table_info
                if version_id_table_info:
                    version_id = version_id_table_info.get('version_id')
        except Exception as e:
            print(f"Exception Occurred:Unable to get versions id in function : {e}")    
            sys.exit(-1)     
    else:
        # pass
        return(version_id)
    return (version_id)   

##################################################################################################
# Function Name  : store_sdd_compliance_checker_info
# Arguments      : csv_row, server, db_tables, cursor,project_id,variant_id,type_id,sw_component_id,customer_id,branch_id,version_id
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to store data in sdd compliance checker info table.
##################################################################################################
def  store_sdd_compliance_checker_info(csv_row, server, db_tables, cursor,project_id,variant_id,type_id,sw_component_id,customer_id,branch_id,version_id):
    # Checking if type is not blank in csv row.
    if csv_row[db_map['type'] ]:
        sdd_compliance_checker_info=""
        sdd_type = f"'{csv_row[db_map['type']]}'"
        script_execution_time=f"'{csv_row[db_map['script_execution_time']]}'"
        try: 
            ## IN FUTURE BELOW SELECT CONDITION. 
        
            # if('Release' in sdd_type):
            #     select_condition =  f"[project_id]={project_id} and [type_id]={type_id} and [sw_component_id]={sw_component_id} and [customer_id]={customer_id} and [version_id]={version_id} and [variant_id] is NULL"
            # elif('Development' in sdd_type):
            #     if version_id =="NULL" and variant_id =="NULL":
            #         select_condition = f"[project_id]={project_id} and [script_execution_time]={script_execution_time} and [type_id]={type_id} and [sw_component_id]={sw_component_id} and [branch_id]={branch_id} and [customer_id]={customer_id} and [version_id]={version_id} and [variant_id] is NULL"
            #     else:
            #         select_condition = f"[project_id]={project_id} and [script_execution_time]={script_execution_time} and [type_id]={type_id} and [sw_component_id]={sw_component_id} and [branch_id]={branch_id} and [customer_id]={customer_id} and [variant_id] ={variant_id} and [version_id]={version_id}"
            
            # print("SDD compliance checker info  select condition --------------->",select_condition)

            ## SHORT LOGIC 
            # Getting the select condition for sdd_compliance_checker_info table From config file.
            # if(variant_id =="NULL"):
            #     # Getting the select condition for Customer table from config file.
            #     select_condition =  f"[type_id]={type_id}  and [customer_id]={customer_id} and [variant_id] is NULL"
            # else :
            #     select_condition =  f"[type_id]={type_id} and  [customer_id]={customer_id} and [variant_id]={variant_id}"

             
            # Getting the select condition for sdd_compliance_checker_info table From config file.
            # TODO Check if variant id present but version id not condition
            if(variant_id =="NULL"):
                # Getting the select condition for Customer table from config file.
                select_condition =  f"[script_execution_time]={script_execution_time} and [project_id]={project_id} and [type_id]={type_id} and [branch_id]={branch_id} and [sw_component_id]={sw_component_id} and [customer_id]={customer_id} and [variant_id] is NULL and [version_id]={version_id}"
            else :
                select_condition =  f"[script_execution_time]={script_execution_time} and [project_id]={project_id} and [type_id]={type_id} and [branch_id]={branch_id} and [sw_component_id]={sw_component_id} and [customer_id]={customer_id} and [variant_id]={variant_id} and [version_id]={version_id}"
        
            sdd_compliance_checker_info = lib.get_table_info (db_tables['sdd_compliance_checker_info']['name'], cursor, select_condition)
            if not (sdd_compliance_checker_info) :
                # Getting the db_columns & db_values from config file for insert query.
                insert_db_columns = db_tables['sdd_compliance_checker_info']['insert']['db_columns']
                insert_db_values = (db_tables['sdd_compliance_checker_info']['insert']['db_values']).format(**locals())
                # Calling the insert function to store data
                lib.insert_table_info(server, db_tables['sdd_compliance_checker_info']['name'], cursor, insert_db_columns, insert_db_values)
            else:
                if('Release'  in sdd_type):
                    update_data = db_tables['sdd_compliance_checker_info']['update']['data'].format(**locals())
                    update_condition = f"[type_id]={type_id} and [sw_component_id]={sw_component_id} and [customer_id]={customer_id} and [version_id]={version_id} and [variant_id] is NULL"
                    # Calling the update function to store data
                    lib.update_table_info(server, db_tables['sdd_compliance_checker_info']['name'], cursor, update_data, update_condition)
                else:
                    pass
        except Exception as e:
            print(f"Error : Exception Occurred  In sdd compliance checker info table query: {e}")    
            sys.exit(-1)     
    else:
        pass


################################################################################
# Function Name  : store_sdd_linked_requirements
# Arguments      : csv_row, server, db_table, cursor,type_id,sw_component_id,branch_id,version_id
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to store data in sdd_compliance_checker_info table.
################################################################################
def store_sdd_linked_requirements(csv_row, server, db_table, cursor):
    # Checking if store_sdd_linked_requirements is not blank in csv row.
    if (csv_row[db_map['sdd_linked_req_ids_list']]):
        requirements=""
        try:
            # Checking if sdd_linked_req_ids_list is not blank in csv row.
            sdd_linked_req_ids_list = ""
            sdd_linked_req_ids_list=csv_row[db_map['sdd_linked_req_ids_list']]
            req_list = sdd_linked_req_ids_list.replace("\"[","").replace("]\"","").replace("'","").replace("'","")
            # For converting string to list 
            req_list=req_list.split(",")
            for req in req_list:
                requirements=""
                if(req.strip()):
                    # Select condition to check data if already exists in db table
                    req= req.strip()
                    select_condition =  f"[requirements] = '{req}'"
                    # Calling the select query function from library file.
                    table_info = lib.get_table_info (db_table['sdd_linked_requirements']['name'], cursor, select_condition) 
                    # Getting the sdd_linked_req_ids_list name from table_info
                    if table_info:
                        requirements = table_info.get('requirements')
                    # Insert if requirements is None.
                    if requirements.strip()== "":
                        # Getting the db_columns & db_values from config file for insert query.
                        insert_db_columns = db_table['sdd_linked_requirements']['insert']['db_columns']
                        insert_db_values =  (db_table['sdd_linked_requirements']['insert']['db_values']).format(**locals())
                        # Calling the insert Function to store data
                        lib.insert_table_info(server, db_table['sdd_linked_requirements']['name'], cursor, insert_db_columns, insert_db_values)
                    else:
                        # Do nothing if sdd_linked_req_ids_list name is already present in database 
                        pass
                else:
                    pass
        except Exception as e:
            print(f"Error :Exception Occurred in sdd_linked_requirements table query: {e}")    
            sys.exit(-1)    

################################################################################
# Function Name  : store_requirement_info
# Arguments      : csv_row, server, db_table, cursor
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to store data in store_sdd_linked_requirements table.
################################################################################
def store_requirement_info(csv_row, server, db_tables,cursor,version_id, branch_id, sw_component_id,variant_id,customer_id):
    # Checking if sdd_linked_req_ids_list is not blank in csv row.
    if (csv_row[db_map['sdd_linked_req_ids_list']]):
        try:
            sdd_type = f"'{csv_row[db_map['type']]}'"
            sdd_type=str(sdd_type)
  
            sdd_linked_req_ids_list = ""
            sdd_linked_req_ids_list=csv_row[db_map['sdd_linked_req_ids_list']]
            # Remove brackets, double quotes and single quotes from the list
            req_list = sdd_linked_req_ids_list.replace("\"[","").replace("]\"","").replace("'","").replace("'","")
            # For converting string to list 
            req_list=req_list.split(",")
            for req in req_list:
                if(req.strip()):
                    req_Table_info=""
                    # Select condition to check data if already exists in db table
                    req_id=get_req_id(db_tables, cursor,req.strip()) 
                    
                    # Getting the select condition for requirement info table From config file.
                    if('Release' in sdd_type):
                        req_select_condition =  f"[req_id]={req_id} and [version_id]={version_id} and [sw_component_id]= {sw_component_id}"
                    
                    elif('Development' in sdd_type):
                        if version_id == "NULL":
                            req_select_condition =  f"[req_id]={req_id} and [branch_id]={branch_id} and [sw_component_id]={sw_component_id}"
                        else:
                            req_select_condition =  f"[req_id]={req_id} and [version_id]={version_id} and [branch_id]={branch_id} and [sw_component_id]={sw_component_id}"
                     
                    req_Table_info = lib.get_table_info (db_tables['requirement_info']['name'], cursor, req_select_condition)
                    if not (req_Table_info) :
                        # Getting the db_columns & db_values from config file for insert query.
                        insert_db_columns = db_tables['requirement_info']['insert']['db_columns']
                        insert_db_values = (db_tables['requirement_info']['insert']['db_values']).format(**locals())
                        # Calling the insert function to store data
                        lib.insert_table_info(server, db_tables['requirement_info']['name'], cursor, insert_db_columns, insert_db_values)
                    else:
                        pass
                else :
                    pass
        except Exception as e:
            print("Error:Exception Occured in store_requirement_info ",{e})
    else:
        print("Warning :sdd_linked_req_ids_list column is empty or type column not exist")   

################################################################################
# Function Name  : get_req_id
# Arguments      : csv_row, db_tables, cursor,req
# Return Value   : 0,-1,req
# Called By      : main
# Description    : This function is to get req id from sdd linked requirements table.
################################################################################
def get_req_id(db_tables, cursor,req):
    req_id = ""
    if req :
        try:
            # Getting the select condition for sdd_linked_requirements table from config file.
            select_condition = f"TRIM([requirements]) = '{req}'"
            # Calling the select query function from library file.
            req_id_table_info = lib.get_table_info (db_tables['sdd_linked_requirements']['name'], cursor, select_condition)
            # Getting the req_id from table_info
            if req_id_table_info:
                req_id = req_id_table_info.get('req_id')
        except Exception as e:
            print(f"Error : Exception Occurred Unable to get requirement id from table info in function req_id function: {e}")    
            sys.exit(-1)     
    else:
        return(req_id)
    return (req_id)

################################################################################
# Function Name  : store_release
# Arguments      : csv_row, server, db_tables, cursor,type_id
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to store data in release table.
################################################################################
def store_release(csv_row, server, db_tables, cursor,type_id):
    # Checking if release_adaptive_version is not blank in csv row.
    if csv_row[db_map['release_adaptive_version']]:
        try:
            release_adaptive_version=csv_row[db_map['release_adaptive_version']]
            rel_list = release_adaptive_version.replace("\'","").replace("\"","")
            rel_list = rel_list.split(",")
            for release_number in rel_list:
                if(release_number.strip()):
                    release_num = ""
                    release_number = release_number.strip()
                    select_condition =  f"[release_number] = '{release_number}' and [type_id] = {type_id}"
                    # Calling the select query function from library file.
                    release_table_info = lib.get_table_info (db_tables['sdd_release']['name'], cursor, select_condition)
                    # Getting the type From release_number
                    if release_table_info:
                        release_num = release_table_info.get('release_number')
                    # Insert if release_number is Blank.
                    if release_num.strip() == "":
                        # Getting the db_columns & db_values from config file for insert query.
                        insert_db_columns = db_tables['sdd_release']['insert']['db_columns']
                        insert_db_values = (db_tables['sdd_release']['insert']['db_values']).format(**locals())
                        # Calling the insert function to store data
                        lib.insert_table_info(server, db_tables['sdd_release']['name'], cursor, insert_db_columns, insert_db_values)
                    else:
                        # Do nothing if release is present
                        pass
        except Exception as e:
            print(f"Error : Exception Occurred  in sdd_release table query: {e}")    
            sys.exit(-1)     
    else:
        pass

################################################################################
# Function Name  : get_release_id
# Arguments      : csv_row,db_table, cursor ,release_number
# Return Value   : 0,-1,release_id
# Called By      : main
# Description    : This function is to get release id form release table.
################################################################################
def get_release_id(csv_row,db_tables, cursor,release_number):
    release_id = ""
    # Checking if release adaptive version is not blank in csv row.
    if csv_row[db_map['release_adaptive_version']]:
        try:
            # Getting the select condition for release id table from config file.
            select_condition = f"[release_number] = '{release_number}'"
            # Calling the select query function from library file.
            release_id_table_info = lib.get_table_info (db_tables['sdd_release']['name'], cursor, select_condition)
            # Getting the type from table_info
            if release_id_table_info:
                release_id = release_id_table_info.get('release_id')
        except Exception as e:
            print(f"Error : Exception Occurred Unable to get release id in function get releae id: {e}")    
            sys.exit(-1)     
    else:
        return(release_id)
    return (release_id)

################################################################################
# Function Name  : store_release_info
# Arguments      : csv_row, server, db_table, cursor,release_id,version_id
# Return Value   : 0,-1
# Called By      : main
# Description    : This function is to store data in release info table.
################################################################################
def store_release_info(csv_row,server,db_tables,cursor,version_id):
    if csv_row[db_map['release_adaptive_version']]:
        try:
            release_adaptive_version=csv_row[db_map['release_adaptive_version']]
            rel_list = release_adaptive_version.replace("\'","").replace("\"","")
            rel_list = rel_list.split(",")
            for release_number in rel_list:
                if(release_number.strip()):
                    release_info=""
                    release_id  = get_release_id(csv_row,db_tables, cursor,release_number.strip())
                    select_condition =  f"[release_id] = {release_id} and [version_id] = {version_id}"
                    # Calling the select query function from library file.
                    release_info = lib.get_table_info (db_tables['release_info']['name'], cursor, select_condition)                
                    # Insert if release_info is empty.
                    if not (release_info):
                        # Getting the db_columns & db_values from config file for insert query.
                        insert_db_columns = db_tables['release_info']['insert']['db_columns']
                        insert_db_values = (db_tables['release_info']['insert']['db_values']).format(**locals())
                        # Calling the insert function to store data
                        lib.insert_table_info(server, db_tables['release_info']['name'], cursor, insert_db_columns, insert_db_values)
                    else:
                        # Do nothing if release is present
                        pass
        except Exception as e:
            print(f"Error : Exception Occurred  in release info query: {e}")    
            sys.exit(-1)
    else:
        pass     
    
################################################################################
# Function Name  : process_cmdl_args
# Arguments      : None
# Return Value   : -1 (in case of failure)
# Called By      : main
# Description    : Read command line arguments
################################################################################
def process_cmdl_args():
    global db_user_name, db_password, input_csv_file
    print("\nReading Command Line Arguments...")
    # Reading All Command Line Arguments
    parser = argparse.ArgumentParser(description="Script insert data to DB")
    parser.add_argument("-db_user_name", "--db_user_name", type=str, nargs=1,default=None, required=True,help="Provide User Name")
    parser.add_argument("-db_password", "--db_password", type=str, nargs=1,default=None, required=True,help="Provide DB Password")
    parser.add_argument("-input_csv_file", "--input_csv_file", type=str, nargs=1,default=None, required=True,help="Provide Input CSV File Path")
    try:
        # Assigning the command line arguments to global variables
        args = parser.parse_args()
        db_user_name = args.db_user_name[0]
        db_password = args.db_password[0]
        input_csv_file = args.input_csv_file[0]
    except Exception as e:
        print(f"Error : Exception Occurred Invalid Command Line Arguments :{e}")    
        sys.exit(-1) 

################################################################################
# Function Name  : main
# Arguments      : None
# Return Value   : 0,-1
# Called By      : None
# Description    : This is the main function.
################################################################################
def main():
    global db_server_name, db_user_name, db_password, db_name, input_csv_file, db_map, db_tables
    # Processing command line arguments
    process_cmdl_args()
    # Connecting to mssql Server 
    server = lib.connect_to_mssql_db(db_server_name, db_user_name, db_password, db_name)
    # Getting the cursor instance to run queries
    cursor = server.cursor()
    # Reading input CSV
    csv_data = read_csv(input_csv_file)
    if csv_data:
        # Storing data in database
        print("Storing data in database..")
        for csv_row in csv_data:  
            # Calling the functions to store data in the tables.
            store_projects(csv_row, server, db_tables, cursor)
            project_id = get_project_id(csv_row, db_tables, cursor)
            # print("This is project id ",project_id)
            
            store_autosaar_variant(csv_row, server, db_tables, cursor,project_id)
            variant_id = get_variant_id(csv_row, db_tables, cursor,project_id)
            # print("This is variant id ",variant_id)
            
            store_customers(csv_row, server, db_tables, cursor,variant_id,project_id)
            customer_id = get_customer_id(csv_row, db_tables, cursor,project_id,variant_id)
            # print("This is customer id ",customer_id)

            store_types(csv_row, server, db_tables, cursor,project_id)
            type_id = get_type_id(csv_row, db_tables, cursor)
            # print("This is type id ",type_id)
        
            store_sw_components(csv_row, server, db_tables, cursor,type_id,variant_id,customer_id)
            sw_component_id = get_sw_components_id(csv_row, db_tables, cursor,type_id,variant_id,customer_id)
            # print("This is sw component id ", sw_component_id)
               
            store_dev_branches(csv_row, server, db_tables, cursor,type_id,variant_id,customer_id)
            branch_id = get_dev_branch_id(csv_row, db_tables, cursor,type_id,variant_id,customer_id)
            # print("This is sw component id", branch_id)

            store_versions(csv_row,server,db_tables,cursor,branch_id,sw_component_id)
            version_id = get_version_id(csv_row,db_tables,cursor,branch_id,sw_component_id)

            store_sdd_compliance_checker_info(csv_row, server, db_tables, cursor,project_id,variant_id,type_id,sw_component_id,customer_id,branch_id,version_id)
            
            store_sdd_linked_requirements(csv_row, server, db_tables, cursor)

            # store_requirement_info(csv_row, server, db_tables,cursor,version_id, branch_id, sw_component_id,variant_id,customer_id)
            
            # store_release(csv_row,server,db_tables,cursor,type_id)
        
            # store_release_info(csv_row,server,db_tables,cursor,version_id)
            
        print("Successfully Added Data in Database!")
    else:
        print("No Data in CSV File!")
        sys.exit(-1)

if __name__ == '__main__':
    print("========================== SDD TOOLCHAIN CSV TO DB SCRIPT ==========================")
    main()
