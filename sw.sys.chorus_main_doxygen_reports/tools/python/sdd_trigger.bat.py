import os
import sys

path_to_be_searched = sys.argv[1]
out_put_path = sys.argv[2]

verbose = True #this is feature of the blacked_list
blacked_list_path = os.path.split(os.path.realpath(__file__))[0] + r'\blacked_list.txt'

with open(blacked_list_path, 'r') as black_list_file:
    blacked_list = []
    for element in black_list_file:
        if element[0] != '#':
            blacked_list.append(element[:-1])
def get_cdd_paths(path):
    cdd_path_list = []
    for filepath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename == 'create_detailed_design.bat':
                cdd_path_list.append(filepath)
    return cdd_path_list

#main
cdd_path_list = get_cdd_paths(path_to_be_searched)
with open(out_put_path, 'w') as output:
    output.write('@echo off\n')
    output.write('cd /d %~dp0\n')
    if verbose == True:
        output.write(r'echo "Log file:" > log.txt' + '\n')
    output.write('SET START_DIR=%CD%\n')
    for path in cdd_path_list:
        if (path in blacked_list) == False:
            if verbose == True:
                output.write('echo ' + r'running ..\.' + path + r' >> log.txt' + '\n')
            output.write('cd ' + r'..\.' + path + '\n')
            output.write('call create_detailed_design.bat' + '\n')
            output.write('cd %START_DIR%' + '\n\n')
