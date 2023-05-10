#! usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
# This script is used to extract metrics info from json
# Usage : python extractSDDMetrics.py
#          --user_name = '******'
#          --password = '******' 
#          --output_metrics_csv_file = "output.csv"
#          --output_graph_csv_file="graph.csv"
# Based on different scenario script will return exit code as follows:
#  0: Script Failure.
################################################################################


# Required Libraries
import sys,json
import argparse
import csv
import requests
import re
import os
import extractSDDMetricsConfig
from copy import deepcopy
from datetime import datetime


# Defining Global Parameters
base_url = ""
repo_path = ""
comp_path =  ""
user_name = ""
password = ""
output_metrics_csv_file = ""
output_graph_csv_file = ""
csvHeader = extractSDDMetricsConfig.csv_header
graph_keys = extractSDDMetricsConfig.graph_header
Metrics_dict_list=[]
projects=extractSDDMetricsConfig.projects
temp_dict = {}
metrics_data=""
graph_data=""   
rel_branch_component_names=[]
dev_branch_component_names=[]
rel_branch_component_urls=[]
dev_branch_component_urls=[]
rel_branch_component_version_urls=[]
dev_branch_component_version_urls=[]
metrics_comp_urls=[]
metrics_dev_comp_urls=[]
metrics_dev_comp_stable_urls=[]
metrics_rel_comp_urls=[]
graph_rel_comp_urls=[]
graph_dict_list=[]
temp_graph_dict={}
last_modified_time=''
current_log_time=''
project_name = extractSDDMetricsConfig.project_name
project_name = project_name.strip()


################################################################################
# Function Name  : process_cmdl_args
# Arguments      : None
# Return Value   : exit(0) (in case of failure)
# Called By      : main
# Description    : Read command line arguments
################################################################################
def process_cmdl_args():
    global base_url, repo_path, comp_path, user_name, password, output_metrics_csv_file,output_graph_csv_file

    print("\nReading Command Line Arguments...")

    # Reading All Command Line Arguments
    parser = argparse.ArgumentParser(description="Script Insert component wise data from artifactory to csv...")
    parser.add_argument("-username", "--username", type=str, nargs=1,default=None, required=True,help="Provide User Name")
    parser.add_argument("-password", "--password", type=str, nargs=1,default=None, required=True,help="Provide DB Password")
    parser.add_argument("-output_metrics_csv_file", "--output_metrics_csv_file", type=str, nargs=1,default=None, required=True,help="Provide Input CSV File Path")
    parser.add_argument("-output_graph_csv_file", "--output_graph_csv_file", type=str, nargs=1,default=None, required=True,help="Provide Input graph CSV File Path")

    try:
        # Assigning the Command Line Arguments to Global Variables
        args = parser.parse_args()
        user_name = args.username[0]
        password = args.password[0]
        output_metrics_csv_file = args.output_metrics_csv_file[0]
        output_graph_csv_file = args.output_graph_csv_file[0]

        # Validating 'output_metrics_csv_file' and 'output_graph_csv_file'  Argument
        output_metrics_csv_file = output_metrics_csv_file.strip()
        output_metrics_csv_file = output_metrics_csv_file.replace("/", "\\")
        output_graph_csv_file = output_graph_csv_file.strip()
        output_graph_csv_file = output_graph_csv_file.replace("/", "\\")
        if (output_metrics_csv_file != "" and output_metrics_csv_file != "''") or (output_graph_csv_file != "" and output_graph_csv_file != "''"):
            if (re.search("^[a-zA-Z0-9](?:[a-zA-Z0-9_-]*[a-zA-Z0-9])?\.[a-zA-Z0-9_-]+$", (os.path.basename(output_metrics_csv_file))) != None) or (re.search("^[a-zA-Z0-9](?:[a-zA-Z0-9_-]*[a-zA-Z0-9])?\.[a-zA-Z0-9_-]+$", (os.path.basename(output_graph_csv_file))) != None):
                output_metrics_csv_file = os.path.abspath(output_metrics_csv_file)
                output_metrics_csv_file_Dir = os.path.dirname(output_metrics_csv_file)
                output_graph_csv_file = os.path.abspath(output_graph_csv_file)
                output_graph_csv_file_Dir = os.path.dirname(output_graph_csv_file)
                if os.path.exists(output_metrics_csv_file_Dir):
                    pass
                else:
                    os.makedirs(output_metrics_csv_file_Dir)

                if os.path.exists(output_graph_csv_file_Dir):
                    pass
                else:
                    os.makedirs(output_graph_csv_file_Dir)
            else:
                print(f"Error: {output_metrics_csv_file} OR {output_graph_csv_file} are not a files. Please provide a valid file paths")
                exit(-1)
        else:
            print("Error: output_metrics_csv_file path or output_graph_csv_file not passed as input")
            exit(-1)
    except Exception as e:
        print(f"Exception Occurred: {e}")    
        sys.exit(-1) 

################################################################################
# Function Name  : get_url_status
# Arguments      : url,username, password
# Return Value   : response
# Called By      : main
# Description    : get response from url.
################################################################################
def get_url_status(url,username, password):
    response = requests.get(url, auth=(username, password))
    return(response)

################################################################################
# Function Name  : read_json
# Arguments      : url
# Return Value   : json_data
# Called By      : main
# Description    : read json files from url.
################################################################################
def read_json(url):
    global last_modified_time
    last_modified_time=''
    auth = (user_name, password)
    response = requests.get(url, auth=auth)
    if response.ok:
        last_modified_str = response.headers['Last-Modified']
        last_modified_time = datetime.strptime(last_modified_str, '%a, %d %b %Y %H:%M:%S %Z')
        json_data = response.json()
        return(json_data)
    else:
        print(f'Request failed with status code {response.status_code}')

################################################################################
# Function Name  : store_csv
# Arguments      : csvheader, job_info, csv_file
# Return Value   : exit(0) in case of failure
# Called By      : main
# Description    : Convert build_info dictionary to csv file.
################################################################################
def store_csv(csvheader,data_list,csv_file):
    # csv_header names to be printed
    # Map column name to alias names. Change names of header column

    print("Preparing csv file...")
    csv_Header=[]
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            for key in csvheader:
                csv_Header.append(csvheader[key])
            csv_writer.writerow(csv_Header)

            for metrics_info in (data_list):
                data = []
                for i in csvheader:
                    if i in metrics_info:
                        data.append(metrics_info[i])
                    else:
                        data.append("")
                csv_writer.writerow(data)
        print(f" {csv_file} file generated successfully!")

    except IOError:
        print("Exception occurred : I/O error file. CSV File already in use")
        exit(-1)
        

################################################################################
# Function Name  : get_components
# Arguments      : data
# Return Value   : components
# Called By      : main
# Description    : get compüonents list.
################################################################################
def get_components(data):
    components = []
    for component in data.get('children', []):
        if component['folder']:
           # Append component names
           components.append(component['uri'])
    return(components)

################################################################################
# Function Name  : get_components_url
# Arguments      : comp_names,base_url,repo_path,comp_path
# Return Value   : components
# Called By      : main
# Description    : get compüonent url response list.
################################################################################
def get_components_url(comp_names,base_url,repo_path,comp_path):
    url_list=[]
    for name in comp_names:
        if name !='':
            component_path = f'{repo_path}/{comp_path}/{name.replace("/","")}'
            url = f'{base_url}/{component_path}'
            url_list.append(url)
    return(url_list)
    
################################################################################
# Function Name  : get_component_versions
# Arguments      : data
# Return Value   : components
# Called By      : main
# Description    : get compüonent versions list.
################################################################################
def get_component_versions(data):
    versions = []
    versions = [version['uri'] for version in data.get('children', [])]
    return(versions)
    
################################################################################
# Function Name  : get_component_versions_urls
# Arguments      : url
# Return Value   : components
# Called By      : main
# Description    : get compüonent versions list.
################################################################################
def get_component_versions_urls(url):
    versions_urls=[]
    response =get_url_status(url,user_name, password)
    if response.status_code != 200:
        print(f'Error: {response.status_code} - {response.text}')
    else:
        # Get component version names
        data=response.json()
        version_names =[]
        version_names = get_component_versions(data) # Get all component versions in list
        for version_name in version_names:
            versions_url = f'{url}/{version_name.replace("/","")}'
            versions_urls.append(versions_url)
    return(versions_urls)
    
    
################################################################################
# Function Name  : normalize_metrics_data
# Arguments      : url,data,sw_type,sw_component,sw_component_rel_version,branch,branch_version
# Return Value   : new_data
# Called By      : main
# Description    : convert metrics data to dictonary format.
################################################################################
def normalize_metrics_data(url,data,sw_type,sw_component,sw_component_rel_version,branch,branch_version):
    global graph_dict_list
    global last_modified_time,current_log_time,project_name
    compliance_report_url=url.replace('metrics.json','sdd-compliance-report.json')
    
    new_data = dict()
    new_data['project_name'] = project_name
    new_data['script_execution_time'] = current_log_time
    new_data['artifactory_upload_time'] = last_modified_time
    new_data['release_adaptive_version'] = ''
    new_data['type'] = sw_type
    new_data['sw_component'] = sw_component
    new_data['sw_component_rel_version'] = sw_component_rel_version 
    new_data['branch'] = branch
    new_data['branch_version'] = branch_version
    new_data['compliance_report'] = compliance_report_url
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
# Function Name  : store_metrics_data
# Arguments      : url,sw_type,sw_component,sw_component_rel_version,branch,branch_version
# Return Value   : new_data
# Called By      : main
# Description    : store all metrics data in list.
################################################################################
def store_metrics_data(url,sw_type,sw_component,sw_component_rel_version,branch,branch_version):
    global temp_dict, Metrics_dict_list
    response = requests.get(url, auth=(user_name, password))      
    if response.status_code == 200:
        # Read raw metrics data
        updated_url = url.replace("api/storage/", "")
        
        metrics_data=read_json(updated_url)
                        
        if metrics_data == "":
            # Clean temparory metrics data
            for key in temp_dict:
                temp_dict[key] = ''
        else:
            # Convert raw metrics data to required dictonary format
            temp_dict=normalize_metrics_data(updated_url,metrics_data,sw_type,sw_component,sw_component_rel_version,branch,branch_version)
            # append organised metrics data to list
            Metrics_dict_list.append(deepcopy(temp_dict))
            # Clean temparory metrics data
            for key in temp_dict:
                temp_dict[key] = ''


################################################################################
# Function Name  : store_graph_data
# Arguments      : url
# Return Value   : None
# Called By      : main
# Description    : store all graph data in list.
################################################################################
def store_graph_data(url):
    global graph_dict_list,temp_graph_dict,graph_data,graph_keys
    response = requests.get(url, auth=(user_name, password))      
    if response.status_code == 200:
        # Read raw metrics data
        updated_url = url.replace("api/storage/", "")
        
        graph_data=read_json(updated_url)
        # print(graph_data)
        for dict_data in graph_data:           
            if dict_data == "":
                # Clean temparory metrics data
                for key in temp_graph_dict:
                    temp_graph_dict[key] = ''
            else:
                new_data = dict()
                for key, value in dict_data.items():
                    if isinstance(value, list):
                        if key == "required_by":
                            comp_list=[]
                            for comp in value:
                                comp_list.append(comp.split('@')[0])
                            new_data[key] = '"'+str(comp_list)+'"'
                        else:
                            new_data[key] = '"'+str(value)+'"'
                    else:
                        if key == "display_name":
                            new_data['component_name'] = (value.split('@')[0]).split('/')[0].strip()
                            new_data['component_version']=(value.split('@')[0]).split('/')[1].strip()
                        else:
                            new_data[key] = value
                temp_graph_dict=new_data
                    
                # append organised metrics data to list
                graph_dict_list.append(deepcopy(temp_graph_dict))
                # Clean temparory metrics data
                for key in temp_graph_dict:
                    temp_graph_dict[key] = ''

        
################################################################################
# Function Name  : get_all_components_url
# Arguments      : projects
# Return Value   : components
# Called By      : main
# Description    : get all components url list from project repository.
################################################################################
def get_all_components_url(projects):
    global base_url,repo_path,comp_path
    global rel_branch_component_names, rel_branch_component_urls
    global dev_branch_component_urls, dev_branch_component_names
    
    for key in projects.keys():
        base_url = projects[key]['base_url']
        repo_path = projects[key]['repo_path']
        comp_path = projects[key]['comp_path']

        url = f'{base_url}/{repo_path}/{comp_path}'
        
        # get response from url
        url_status=get_url_status(url,user_name, password)
        if url_status.status_code != 200:
            print(f'Error: {url_status.status_code} - {url_status.text}')
            exit(-1)
            
        print(f'Geting components url from {url} ...')
        if key == 'development':
            # Get component names
            data=url_status.json()
            dev_branch_component_names=get_components(data) # Get all components in list
            dev_branch_component_urls=get_components_url(dev_branch_component_names,base_url,repo_path,comp_path)
        else:
            # Get component names
            data=url_status.json()
            rel_branch_component_names=get_components(data) # Get all components in list
            rel_branch_component_urls=get_components_url(rel_branch_component_names,base_url,repo_path,comp_path)

################################################################################
# Function Name  : get_all_dev_branch_metrics_url
# Arguments      : data
# Return Value   : None
# Called By      : main
# Description    : get all metrics.json url from development branch.
################################################################################
def get_all_dev_branch_metrics_url():
    global dev_branch_component_urls, dev_branch_component_version_urls
    global metrics_dev_comp_urls, metrics_dev_comp_stable_urls

    for dev_branch_component_url in dev_branch_component_urls:
        dev_branch_component_version_urls=get_component_versions_urls(dev_branch_component_url)
        for dev_branch_component_version_url in dev_branch_component_version_urls:
            if dev_branch_component_version_url.split('/')[-1]=='stable':
                dev_comp_stable_versions_urls=get_component_versions_urls(dev_branch_component_version_url)
                for dev_comp_stable_versions_url in dev_comp_stable_versions_urls:
                    metrics_dev_comp_stable_urls.append(f'{dev_comp_stable_versions_url}/SDD/generated/sdd-compliance-checker/metrics.json')
            else:
                metrics_dev_comp_urls.append(f'{dev_branch_component_version_url}/SDD/generated/sdd-compliance-checker/metrics.json')


################################################################################
# Function Name  : get_all_rel_branch_metrics_url
# Arguments      : data
# Return Value   : None
# Called By      : main
# Description    : get all metrics.json url from release branch.
################################################################################
def get_all_rel_branch_metrics_url():
    global metrics_rel_comp_urls, graph_rel_comp_urls
    global rel_branch_component_version_urls, rel_branch_component_urls
    
    for rel_branch_component_url in rel_branch_component_urls:
        rel_branch_component_version_urls=get_component_versions_urls(rel_branch_component_url)
        for rel_branch_component_version_url in rel_branch_component_version_urls:
            metrics_rel_comp_urls.append(f'{rel_branch_component_version_url}/SDD/generated/sdd-compliance-checker/metrics.json')
            graph_rel_comp_urls.append(f'{rel_branch_component_version_url}/graph.json')
            
################################################################################
# Function Name  : store_rel_branch_metrics_data
# Arguments      : url_list
# Return Value   : None
# Called By      : main
# Description    : get all metrics.json data from release branch.
################################################################################
def store_rel_branch_metrics_data(url_list):
    for url in url_list:
        sw_type = 'Release'
        sw_component = (url.split('/SDD/generated/')[0]).split('/')[-2]
        sw_component_rel_version = (url.split('/SDD/generated/')[0]).split('/')[-1] 
        branch = ''
        branch_version = ''
        
        store_metrics_data(url,sw_type,sw_component,sw_component_rel_version,branch,branch_version)


################################################################################
# Function Name  : store_rel_branch_graph_data
# Arguments      : url_list
# Return Value   : None
# Called By      : main
# Description    : get all graph.json data from release branch.
################################################################################
def store_rel_branch_graph_data(url_list):
    for url in url_list:
        store_graph_data(url)


################################################################################
# Function Name  : store_dev_branch_metrics_data
# Arguments      : url_list
# Return Value   : None
# Called By      : main
# Description    : get all metrics.json data from development branch.
################################################################################
def store_dev_branch_metrics_data(url_list):
    for url in url_list:
        sw_type = 'Development'
        sw_component = (url.split('/SDD/generated/')[0]).split('/')[-2]
        sw_component_rel_version = '' 
        branch = (url.split('/SDD/generated/')[0]).split('/')[-1]
        branch_version = ''
        
        store_metrics_data(url,sw_type,sw_component,sw_component_rel_version,branch,branch_version)
        
################################################################################
# Function Name  : store_dev_branch_stable_metrics_data
# Arguments      : url_list
# Return Value   : None
# Called By      : main
# Description    : get all metrics.json data from development branch stable component.
################################################################################
def store_dev_branch_stable_metrics_data(url_list):
    for url in url_list:
        sw_type = 'Development'
        sw_component = (url.split('/SDD/generated/')[0]).split('/')[-3]
        sw_component_rel_version = '' 
        branch = (url.split('/SDD/generated/')[0]).split('/')[-2]
        branch_version = (url.split('/SDD/generated/')[0]).split('/')[-1]
        
        store_metrics_data(url,sw_type,sw_component,sw_component_rel_version,branch,branch_version)
    
################################################################################
# Function Name  : main
# Arguments      : None
# Return Value   : 0,-1
# Called By      : None
# Description    : This is the main function.
################################################################################
def main():
    global base_url, repo_path, comp_path, user_name, password, output_metrics_csv_file,projects,output_graph_csv_file
    global Metrics_dict_list, csvHeader, temp_dict
    global metrics_data, metrics_comp_urls,metrics_dev_comp_urls, metrics_dev_comp_stable_urls, metrics_rel_comp_urls
    global rel_branch_component_names,rel_branch_component_version_urls, rel_branch_component_urls
    global dev_branch_component_urls, dev_branch_component_names, dev_branch_component_version_urls
    global graph_rel_comp_urls, graph_dict_list,temp_graph_dict,graph_keys,current_log_time
   
    
    # Processing Command Line Arguments
    process_cmdl_args()
    current_date_time = datetime.now()
    current_date_time_timestamp = current_date_time.timestamp()
    current_log_time = datetime.utcfromtimestamp(current_date_time_timestamp)
    try:
        # Get all components url of projects configured in extract_metrics_json_config.py from artifactory
        get_all_components_url(projects)
        
        # Get all projects components of development path's metrics.json file url from artifactory
        print(f'Getting metrics.json url from development branch\'s components ...')
        get_all_dev_branch_metrics_url()
        
        # Get all projects components of release path's metrics.json file url from artifactory
        print(f'Getting metrics.json url from release branch\'s components ...')
        get_all_rel_branch_metrics_url()
        
        # Store all projects components of release path's graph.json file data
        print(f'Storing graph.json data from release branch\'s components ...')
        store_rel_branch_graph_data(graph_rel_comp_urls)
        
        # Store all projects components of release path's metrics.json file data
        print(f'Storing metrics.json data from release branch\'s components ...')
        store_rel_branch_metrics_data(metrics_rel_comp_urls)
        
        # Store all projects components of development path's metrics.json file data
        print(f'Storing metrics.json data from development branch\'s components ...')
        store_dev_branch_metrics_data(metrics_dev_comp_urls)
        
        # Store all projects stable component of development path's metrics.json file data
        print(f'Storing metrics.json data from development branch\'s stable components ...')
        store_dev_branch_stable_metrics_data(metrics_dev_comp_stable_urls)   
        
        # Store metrics data to csv file
        store_csv(csvHeader,Metrics_dict_list,output_metrics_csv_file)

        # Store graph metrics data to csv file
        store_csv(graph_keys,graph_dict_list,output_graph_csv_file)
        
    except Exception as e:
        print(f"Exception Occurred: {e}")
        
 
if __name__ == '__main__':
    print("========================== Artifactory Metrics data TO CSV SCRIPT ==========================")
    main()

