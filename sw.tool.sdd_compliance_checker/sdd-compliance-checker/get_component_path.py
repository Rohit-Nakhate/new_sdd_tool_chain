#! /usr/bin/python3
# -*- coding: utf-8 -*-
#################################################################################
#This script is used to get component path and generate csv file 
#Usage: get_component_path.py --input_dir=<INPUT DIR> --output_dir=<OUTPUT DIR>
#  Based on different scenario script will return different exit code as follows:
#  0: Data Inserted Successfully.
# -1: Script Failure.
#################################################################################

#Required libraries
import os
import sys
import csv
import argparse

#Defining global variables
input_dir=""
output_dir=""

################################################################################
# Function Name  : process_cmdl_args
# Arguments      : None
# Return Value   : -1 (in case of failure)
# Called By      : main
# Description    : This function is to Read command line arguments
################################################################################

def process_cmdl_args():
    global input_dir , output_dir
    
    print("\nReading Command Line Arguments...")

    #Reading Commandline arguments 
    parser = argparse.ArgumentParser(description="Collect paths of directories containing an 'xml' folder in a nested folder structure")
    parser.add_argument("--input_dir" ,required=True , help="Provide path to input dir here " )
    parser.add_argument("--output_dir" ,required=True , help="Provide path to output dir here " )

    try:
        # Assigning the Command Line Arguments to Global Variables
        args = parser.parse_args()
        input_dir = args.input_dir
        output_dir = args.output_dir
        # print(output_dir)
        #Check if output_dir exist 
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except Exception as e:
        print(f"Exception Occurred: Invalid Arguments ",e)    
        sys.exit(-1) 

################################################################################
# Function Name  : collect_path
# Arguments      : input_dir 
# Return Value   : status code  or -1 (in case of failure)
# Called By      : main
# Description    : This function is to collect folder path 
################################################################################

def collect_path(input_dir):
    try:
        collect_xml_path = []
        templist =[]
        for root,dir,file_name in os.walk(input_dir):
            if 'xml' in dir:
                dir_path = os.path.join(root, "xml")
                print(dir_path)
                # Add the path to the list
                templist.append(dir_path)
                outpath = dir_path.replace("doc\\Doxygen\\xml","")
                outpath = outpath.replace("sw.sys.chorus_main_doxygen_reports","sw.sys.chorus_main_doxygen_reports\\output")
                templist.append(outpath)
                collect_xml_path.append(templist)
                templist = []
                

        # print("List of xml paths",collect_xml_path)
        return collect_xml_path
    except Exception as e :
        print(f"Exception Occurred:Error while collect folder path ",e)  

################################################################################
# Function Name  : generate_csv
# Arguments      : xml_path_list,output_dir
# Return Value   : status code  or -1 (in case of failure)
# Called By      : main
# Description    : This function is to generate csv in output directory
################################################################################

def generate_csv(xml_path_list,output_dir):
    try:
        #In this function we write logic to data in csv  
        with open(f'{output_dir}\\component_list.csv','w+',newline='') as csv_file:
            writer = csv.writer(csv_file)
            components=["Components","output_path"]
            writer.writerow(components)
            # for items in xml_path_list:
            #     writer.writerow([items])
            writer.writerows(xml_path_list)
    except Exception as e:
        print(f"Exception Occurred: Error while generating csv file",e)  

################################################################################
# Function Name  : main
# Arguments      : None
# Return Value   : 0,-1
# Called By      : None
# Description    : This is the main function.
################################################################################

def main():
    global input_dir , output_dir
    
    #Processing Command Line Arguments
    process_cmdl_args()
    #Calling collect_path function 
    xml_path_list = collect_path(input_dir)
    #Generating csv file function 
    generate_csv(xml_path_list,output_dir)

if __name__=='__main__':
    main()
    print("<-- Script Run Sucessfully -->")
