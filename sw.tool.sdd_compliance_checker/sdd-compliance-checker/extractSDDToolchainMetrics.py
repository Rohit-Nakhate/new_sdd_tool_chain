#! usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
# This script is used to extract metrics info from json
# Usage : python extractSDDMetrics.py
#          --input_csv_file =<CSV FILE> 
#          --output_csv_file=<CSV FILE>
# Based on different scenario script will return exit code as follows:
#  -1: Script Failure.
################################################################################

#Required Libaries
import argparse
import csv
import json 
import os
import sys
from copy import deepcopy
import extractSDDToolchainMetricsConfig as config
from datetime import datetime
import xml.etree.ElementTree as ET
import logging

# Defining Global Parameters
input_csv_file=""  
output_csv_file ="" 
metrics_paths = [] 
input_path =[] 
Metrics_dict_list=[] 
combine_dict_list=[] 
list_components = [] 
csvHeader = config.csv_header
project_name=""
component_name_file = ""
current_log_time = ""
Customer=""
Variant = ""
sw_component=""
sw_component_rel_version=""
artifactory_upload_time=""
release_adaptive_version=""
component_name = False
Customer = False
Project_Name = False
Variant = False

################################################################################
# Function Name  : process_cmdl_args
# Arguments      : None
# Return Value   : exit(-1) (in case of failure)
# Called By      : main
# Description    : Read command line arguments
################################################################################
def process_cmdl_args():
    global  input_csv_file, output_csv_file 
    # output_path=""
    print("\nReading Command Line Arguments...\n")
    parser=argparse.ArgumentParser()
    parser.add_argument("--input_csv_file",type=str, default=None,help="path to CSV inpput file")
    parser.add_argument("--output_csv_file",type=str, default=None,help="path to CSV output file")
    try:
        args = parser.parse_args()
        input_csv_file = args.input_csv_file
        output_csv_file = args.output_csv_file

        # Check if directory exist if not create     
        output = os.path.dirname(output_csv_file)
        if not os.path.exists(output):
            os.makedirs(output)

        script_dir = os.path.dirname(output_csv_file)
        log_file_path = os.path.join(script_dir,'metrics.log')
        # Set up logging configuration
        logging.basicConfig( level=logging.WARNING,filename='D:\\New_task\\cloned_repo\\GIT_CLONE\\new_sdd_tool_chain\\sw.sys.chorus_main_doxygen_reports\\output\\metrics.log',filemode='w',format='%(asctime)s - %(levelname)s - %(message)s')

        # Check if input path exists 
        if not os.path.exists(input_csv_file):
            print("Error Exception Occured csv File Not Exist ",input_csv_file)
            sys.exit(-1)
    except Exception as e:
        print("Error:Exception Occured Invalid Command Line Arguments ",e)
        sys.exit(-1)

################################################################################
# Function Name  : read_json
# Arguments      : None
# Return Value   : json data
# Called By      : get_metrics_data
# Description    : This function is used to read json data from files.
################################################################################
def read_json(path):
    try:
            with open(path,'r') as json_file:
                if json_file != "" and '.json' in path:
                    json_data = json.load(json_file)
                    return json_data
    except Exception as e:
        print("Error : Exception Occured While Reading JSON File At {path} ",e)
    
###################################################################################
# Function Name  : normalize_metrics_data
# Arguments      : data,sw_type,list_components
# Return Value   : new_data
# Called By      : store_metrics_data
# Description    : This function is used to convert metrics data to dictonary format.
####################################################################################
def normalize_metrics_data(data,sw_type,list_components):
    global current_log_time
    try :
        # Calculate Current log time 
        current_date_time = datetime.now()
        current_date_time_timestamp = current_date_time.timestamp()
        current_log_time = datetime.utcfromtimestamp(current_date_time_timestamp)
        new_data = dict()
        # Check if list of components not empty
        if list_components != '':
            # Check if project name in list of list components
            if "project_name" in list_components:
                new_data['project_name'] = list_components['project_name']
            else:
                new_data['project_name'] = ""
            # Check if sw_component name in list of list components
            if "sw_component" in list_components:
                new_data['sw_component']= list_components['sw_component']
            else:
                new_data['sw_component'] = ""
            # Check if Customer name in list of list components
            if "Customer" in list_components:
                new_data['Customer']= list_components['Customer']
            else:
                new_data['Customer'] = ""
            # Check if Variant  in list of list components
            if "Variant" in list_components:
                new_data['Variant']= list_components['Variant']
            else:
                new_data['Variant'] = ""
            if "type" :
                new_data['type']= sw_type
            else:
                new_data['type'] = ""
            if  "script_execution_time":
                new_data['script_execution_time']= current_log_time
            else:
                new_data['type'] = ""

            new_data['artifactory_upload_time'] = ''
            new_data['release_adaptive_version'] = ''

        # Check if data is empty 
        if data != '':
            for key, value in data.items():
                if not isinstance(value, dict):
                    new_data[key] = value
                else:
                    for k, v in value.items():
                        if isinstance(v, list): #sdd_trace_details_nmb_dds_fct
                            new_data[key + "_" + k] = '"'+str(v)+'"'
                        else:
                            if (key + "_" + k) == 'sdd_trace_details_nmb_dd_fct':
                                new_data['sdd_trace_details_nmb_dds_fct'] = v
                            else:
                                new_data[key + "_" + k] = v
        return(new_data)
    except Exception as e:
        print("Error : Exception Occured In Normalize Metrics Data Functoion ",e)

################################################################################
# Function Name  : get_all_path
# Arguments      : None
# Return Value   : exit(-1) (in case of failure)
# Called By      : main
# Description    : This function is used to get all the paths from CSV file.
################################################################################
def get_all_path():
    global input_csv_file , metrics_paths,input_path,combine_dict_list
    try:
        if input_csv_file != "" and '.csv' in input_csv_file:
            with open (input_csv_file,'r') as csv_file:             
                    dict_reader = csv.DictReader(csv_file)
                    # Convert to list of dictionary
                    list_of_dict =list(dict_reader)
                    # Join the paths metrics.json to Output paths and  indexpage.xml to Components paths 
                    for data in list_of_dict:
                        if ('output_path' in data) and ('Components' in data):
                            metrics_paths.append(f"{data['output_path']}metrics.json") 
                            input_path.append(f"{data['Components']}\indexpage.xml")
                    # Check if both list equal in length and not empty
                    if (len(metrics_paths) == len(input_path)) and (metrics_paths != [] and input_path != []):
                        temp_dict={}
                        # Iterate over each index and value in metrics path list
                        for index, val in enumerate(metrics_paths):
                            temp_dict["metrics"]=metrics_paths[index]
                            temp_dict["xml"]=input_path[index]
                            # Append the dictionary object to temp_dict dictionary
                            combine_dict_list.append(deepcopy(temp_dict))
        else:
            print("Error : Exception Occured Invalid CSV File ",e)
            sys.exit(-1)
    except Exception as e :
        print("Error : Exception Occured Invalid Input CSV File ",e)
        sys.exit(-1)
##################################################################################
# Function Name  : extract_data
# Arguments      : elem
# Return Value   : None
# Called By      : get_all_path
# Description    : This function is used to extract all components from XML files.
##################################################################################
def extract_data(elem,key,temp_dict):
    global component_name,Customer,Project_Name,Variant,list_components
    try:
        # Iterating on tags in XML file to extract values
        component_name_elem = next(elem.iter("para"))
        component_element = str(component_name_elem.text)
        # Removing white spaces from traling end  
        component_element=component_element.strip()
        # Check if tag nested tags present
        if(component_name_elem.text == None):
            bold = component_name_elem.find('bold')
            # Append to dictionary
            temp_dict[key]=bold.text
        else:
            # Append to dictionary
            temp_dict[key]=component_element

        # Reset the flags
        if component_name == True:
            component_name = False
        elif Customer == True:
            Customer = False
        elif Project_Name == True:
            Project_Name = False
        elif Variant == True:
                Variant = False
    except Exception as e:
        print("Error:Exception Occured while extracting values from XML In Extract Data Function ",e)
 
################################################################################
# Function Name  : get_component_info
# Arguments      : component_xml
# Return Value   : temp_dict 
# Called By      : get_metrics_data
# Description    : This function is used to Get all the components from XML file.
################################################################################
def get_component_info(component_xml):
    global component_name,Customer,Project_Name,Variant
    # Parse the XML file
    temp_dict={}
    tree = ET.parse(component_xml)
    # Get the root element
    root = tree.getroot()
    # Iterating on root element in XML file
    for elem in root.iter():
        if component_name == True:
            # Extract Component name from XML file
            extract_data(elem,key,temp_dict)
        if Customer == True:
            # Extract Customer name from XML file
            extract_data(elem,key,temp_dict)
        if Project_Name == True:
            # Extract Project name from XML file
            extract_data(elem,key,temp_dict)
        if Variant == True:
        # Extract Variant  from  XML file
            extract_data(elem,key,temp_dict)

        # Check if tag is present with required value
        if elem.tag == 'para' and str(elem.text).strip() == 'Component Name':
            key = 'sw_component'
            component_name = True
        # Check if tag is present with required value
        if elem.tag == 'para' and str(elem.text).strip() == 'Customer':
            key = 'Customer'
            Customer = True
        # Check if tag is present with required value
        if elem.tag == 'para' and str(elem.text).strip() == 'Project Name':
            key ='project_name'
            Project_Name = True
        # Check if tag is present with required value
        if elem.tag == 'para' and str(elem.text).strip() == 'Variant':
            key ='Variant'
            Variant = True
    return(temp_dict)

################################################################################
# Function Name  : get_metrics_data
# Arguments      : None
# Return Value   : None
# Called By      : main
# Description    : This function is used to get all metrics JSON file data 
################################################################################
def get_metrics_data():
    global combine_dict_list
    try:
        list_of_comps=""
        metrics_data=""
        # Iterating on combine dictionary XML and JSON file path
        for data in combine_dict_list:
            for key in data:
                if key == "metrics":
                    # Check metrics JSON file path exist
                    if not os.path.exists(data[key]):
                        #TODO
                        # print("##################################")
                        print(f"{data[key]} File not found....")
                        logging.warning(f"{data[key]} File not found....")
                        # print("##################################\n")
                    else:
                        # Reading json file  
                        metrics_data = read_json(data[key])
                        # print(metrics_data)

                if key == "xml":
                    # Check metrics XML file path exist
                    if not os.path.exists(data[key]):
                        # print("##################################")
                        print(f"{data[key]} File not found....")
                        logging.warning(f"{data[key]} File not found....")
                        # print("##################################\n")
                    else:
                        # Call get component name to extract component name from XML file
                        list_of_comps=get_component_info(data[key])
            # Store data form JSON and XML file              
            store_metrics_data(metrics_data,list_of_comps)
            metrics_data=""
            # Clean temparory metrics data
            for key in list_of_comps:
                list_of_comps[key] = ''
    except Exception as e :
        print("Error: Exception Occured In The Function Get Metrics Data Function",e)
################################################################################
# Function Name  : store_metrics_data
# Arguments      : metrics_data,list_components
# Return Value   : None
# Called By      : get_metrics_data
# Description    : This function is used to Store metrics data 
################################################################################
def store_metrics_data(metrics_data,list_components):
    global Metrics_dict_list
    try:
        # Check if xml and json file not present 
        # Check if data is not empty in metrics data list and list of components
        if (metrics_data !="" and list_components !=""):
            # Convert raw metrics data to required dictonary format
            temp_dict=normalize_metrics_data(metrics_data,"Development",list_components)
            # append organised metrics data to list
            Metrics_dict_list.append(deepcopy(temp_dict))
            # Clean temparory metrics data
            for key in temp_dict:
                temp_dict[key] = ''
    except Exception as e:
        print("Error : Exception Occured While Storing Metrics Data In Store Metrics Data Function",e)

################################################################################
# Function Name  : store_csv
# Arguments      : csvheader, job_info, csv_file
# Return Value   : exit(-1) in case of failure
# Called By      : main
# Description    : This function is used to generate CSV and store data in the CSV File .
################################################################################
def store_csv(csvHeader,data_list,output_csv_file):
    # csv_header names to be printed
    # Map column name to alias names. Change names of header column
    print("Preparing csv file...")
    csv_Header=[]
    try:
        # File 
        with open(output_csv_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            for key in csvHeader:
                csv_Header.append(csvHeader[key])
            # Writing headers in CSV file    
            csv_writer.writerow(csv_Header)

            # Iterating on data list
            for metrics_info in (data_list):
                data = []
                for i in csvHeader:
                    if i in metrics_info:
                        # Appending data to data  list  
                        data.append(metrics_info[i])
                    else:
                        data.append("")
                csv_writer.writerow(data)
        
        script_dir = os.path.dirname(output_csv_file)
      
        # Set up logging configuration
        logging.basicConfig( level=logging.WARNING,filename='metrics.log',filemode='w',format='%(asctime)s - %(levelname)s - %(message)s')
        log_file_path = os.path.join(script_dir,'metrics.log')
    
        # print(f"{output_csv_file} File Generated Successfully!")
        print("File Generated Successfully!")
    except Exception as e:
        print("Error:Exception Occurred While Generating CSV File In Store CSV Function",e)
        exit(-1)
################################################################################
# Function Name  : main
# Arguments      : None
# Return Value   : 0,-1
# Called By      : None
# Description    : This is the main function.
################################################################################            
def main():
    global Metrics_dict_list,output_csv_file,csvHeader,output_csv_file
try:

    # Processing commandline arguments 
    process_cmdl_args()

    # Collecting all paths in list
    get_all_path()
    
    # Collecting metrics.json data in dict
    get_metrics_data()
    # Generating output and storing data in CSV File
    store_csv(csvHeader,Metrics_dict_list,output_csv_file)
except Exception as e:
    print(f"Exception Occurred: {e}")
        
if __name__=="__main__":
    main()
