#! usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
# This script is used to extract metrics info from json
# Usage : python extractSDDMetrics.py
#          --output_csv = "output.csv"
#          --input_metrics_csv_file="metrics.json"
# Based on different scenario script will return exit code as follows:
#  0: Script Failure.
################################################################################

#Required Libaries
import argparse
import csv
import json 
import os
import sys
from copy import deepcopy

# Defining Global Parameters
input_file=""
input_csv_file=""
output_csv_file =""
project_name = "SDDToolchain"
metrics_paths = []
Metrics_dict_list=[]
################################################################################
# Function Name  : process_cmdl_args
# Arguments      : None
# Return Value   : exit(-1) (in case of failure)
# Called By      : main
# Description    : Read command line arguments
################################################################################
def process_cmdl_args():
    global  input_csv_file, output_csv_file
    print("\nReading Command Line Arguments...")
    parser=argparse.ArgumentParser()
    parser.add_argument("--input_csv_file",type=str, default=None,help="path to CSV inpput file")
    parser.add_argument("--output_csv_file",type=str, default=None,help="path to CSV output file")
    try:
        args = parser.parse_args()
        input_csv_file = args.input_csv_file
        output_csv_file = args.output_csv_file

        if not os.path.exists(output_csv_file):
            os.mkdir(output_csv_file)

        if not os.path.exists(input_csv_file):
            print("Error Exception occured csv file not exist ",input_csv_file)
            sys.exist(-1)

    except Exception as e:
        print("Error Occured:Invalid Arguments ",e)
        sys.exit(-1)


################################################################################
# Function Name  : read_json
# Arguments      : 
# Return Value   : 
# Called By      : main
# Description    : read json files from .
################################################################################
def read_json(path):
   with open(path,'r') as json_file:
       json_data = json.load(json_file)
       return json_data
      
################################################################################
# Function Name  : generate_csv
# Arguments      : 
# Return Value   : 
# Called By      : main
# Description    : Generate output.csv file.
################################################################################
def generate_csv():
    global Metrics_dict_list
    keys = Metrics_dict_list[0].keys()
    # TODO : remove hardcoded
    with open(f"{output_csv_file}\\matrics.csv", 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(Metrics_dict_list)


################################################################################
# Function Name  : normalize_metrics_data
# Arguments      : sw_type,sw_component,sw_component_rel_version,branch,branch_version
# Return Value   : new_data
# Called By      : main
# Description    : convert metrics data to dictonary format.
################################################################################
def normalize_metrics_data(data,sw_type,sw_component):
    global current_log_time,project_name
    new_data = dict()
    new_data['project_name'] = project_name
    # new_data['script_execution_time'] = current_log_time
    new_data['type'] = sw_type
    new_data['sw_component'] = sw_component

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

################################################################################
# Function Name  : get_all_path
# Arguments      : None
# Return Value   : 
# Called By      : main
# Description    : 
################################################################################
def get_all_path():
    global input_csv_file , metrics_paths
    with open (input_csv_file,'r') as csv_file:
        csv_file = csv.reader(csv_file) 
        for items in csv_file:
            if 'output_path' in items   :
                continue
            metrics_paths.append(items[1])

################################################################################
# Function Name  : get_metrics_data
# Arguments      : None
# Return Value   : 
# Called By      : main
# Description    : 
################################################################################
def get_metrics_data():
    global metrics_paths
    for path in metrics_paths:
        new_path = os.path.join(path,"metrics.json")
        if not os.path.exists(new_path):
            continue
        store_metrics_data(new_path)

################################################################################
# Function Name  : store_metrics_data
# Arguments      : None
# Return Value   : 
# Called By      : main
# Description    : 
################################################################################
def store_metrics_data(path):
    metrics_data = read_json(path)
    if metrics_data == "":
        # Clean temparory metrics data
        for key in temp_dict:
            temp_dict[key] = ''
    else:
        # Convert raw metrics data to required dictonary format
        temp_dict=normalize_metrics_data(metrics_data,"Dev","ICAS")
        # append organised metrics data to list
        Metrics_dict_list.append(deepcopy(temp_dict))
        # Clean temparory metrics data
        for key in temp_dict:
            temp_dict[key] = ''

################################################################################
# Function Name  : main
# Arguments      : None
# Return Value   : 0,-1
# Called By      : None
# Description    : This is the main function.
################################################################################            
def main():
    global Metrics_dict_list
    # Processing commandline arguments 
    process_cmdl_args()

    # Collecting all paths in list
    get_all_path()
    
    #collecting metrics.json data in dict
    get_metrics_data()

    #Generating output csv file
    generate_csv()
    # print(Metrics_dict_list)

if __name__=="__main__":
    main()
