import os
import re
import sys

#a function that when given a name of a file and a rootpath
#it will return a list that contains all the path with the given name
def findfile(root, name):
    path_list = []
    for (relpath, dirs, files) in os.walk(root):
        if name in files:
            path_list.append(relpath)
    return path_list

if __name__ == '__main__':
    #check the arguments number in export.bat
    if len(sys.argv) >= 2:
        path_to_doxygen = sys.argv[1]
        xmlprj_output_file = sys.argv[2]
        variant = sys.argv[3]
    else:
        print('Error: the number of arguments is not enough\n')
        exit()

    end_of_line = '\n'
    merge_xsl_list = []
    merge_xsl_list.append(r'<?xml version="1.0" encoding="UTF-8"?>' + end_of_line)
    merge_xsl_list.append(r'<project xmlns:xi="http://www.w3.org/2003/XInclude" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' + end_of_line)
    merge_xsl_list.append(r'   <files>' + end_of_line)

    path_list = findfile(path_to_doxygen, 'index.xml')

    for i in range(len(path_list)):
        splited_path = re.split(r'[\\]', path_list[i])#for selecting the swc_name
        rel_variant_path = '\\'+variant+'\\doc\\Doxygen\\xml'
        if (rel_variant_path in path_list[i]):
            swc_name = splited_path[splited_path.index(variant) - 1]
            merge_xsl_list.append(r'      <SDD>' + end_of_line)
            merge_xsl_list.append(r'            <xi:include href="' + swc_name + r'.xml" parse="xml"/>' + end_of_line)
            merge_xsl_list.append(r'      </SDD>' + end_of_line)
        rel_variant_path='\\c\\doc\\Doxygen\\xml'
        if (rel_variant_path in path_list[i]):
            swc_name = splited_path[splited_path.index('c') - 1]
            merge_xsl_list.append(r'      <SDD>' + end_of_line)
            merge_xsl_list.append(r'            <xi:include href="' + swc_name + r'.xml" parse="xml"/>' + end_of_line)
            merge_xsl_list.append(r'      </SDD>' + end_of_line)

    merge_xsl_list.append(r'   </files>' + end_of_line)
    merge_xsl_list.append(r'</project>' + end_of_line)

    SDD_ICAS_file = open(xmlprj_output_file, 'w')
    SDD_ICAS_file.writelines(merge_xsl_list)
    SDD_ICAS_file.close