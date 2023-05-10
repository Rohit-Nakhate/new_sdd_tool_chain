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
        merge_output_file = sys.argv[2]
        variant = sys.argv[3]
    else:
        print('Error: the number of arguments is not enough')
        exit()

    end_of_line = '\n'
    merge_list = []#create a list for the generating file
    merge_list.append(r'@echo off' + end_of_line)
    merge_list.append(r'rem set ts_mirr_path=%TS_LOCAL%' + end_of_line)
    merge_list.append(r'rem set JAVA=%ts_mirr_path%\xml\jre1.5.0\bin\java.exe -Duser.language=en -Xmx256m' + end_of_line)
    merge_list.append(r'rem set XALANPATH=-Djava.endorsed.dirs="%ts_mirr_path%\xml\xerces2.6.2;%ts_mirr_path%\xml\xalan2.6.0;%ts_mirr_path%\xml\saxon-b"' + end_of_line)
    merge_list.append(r'rem set XINCLUDE=-Dorg.apache.xerces.xni.parser.XMLParserConfiguration=org.apache.xerces.parsers.XIncludeParserConfiguration' + end_of_line)
    merge_list.append(r'rem set XALAN=net.sf.saxon.Transform' + end_of_line)
    merge_list.append(r'rem set VALIDATE=net.sf.saxon.Validate' + end_of_line)

    path_list = findfile(path_to_doxygen, 'index.xml')

    for i in range(len(path_list)):
        splited_path = re.split(r'[\\]', path_list[i])#for selecting the swc_name
        rel_variant_path = '\\'+variant+'\\doc\\Doxygen\\xml'
        if (rel_variant_path in path_list[i]):
            swc_name = splited_path[splited_path.index(variant) - 1]
            merge_list.append(end_of_line + 'set SWC_NAME=' + swc_name + end_of_line)
            merge_list.append('set PATH_TO_SWC=' + path_list[i] + end_of_line)
            merge_list.append('echo Merging %SWC_NAME%' + end_of_line)
            merge_list.append(r'%JAVA% %XALANPATH% %XINCLUDE% %XALAN% -s:%PATH_TO_SWC%\index.xml -xsl:%PATH_TO_SWC%\combine.xslt -o:temp\\' + variant +r'\%SWC_NAME%.xml' + end_of_line)
        rel_variant_path='\\c\\doc\\Doxygen\\xml'
        if (rel_variant_path in path_list[i]):
            swc_name = splited_path[splited_path.index('c') - 1]
            merge_list.append(end_of_line + 'set SWC_NAME=' + swc_name + end_of_line)
            merge_list.append('set PATH_TO_SWC=' + path_list[i] + end_of_line)
            merge_list.append('echo Merging %SWC_NAME%' + end_of_line)
            merge_list.append(r'%JAVA% %XALANPATH% %XINCLUDE% %XALAN% -s:%PATH_TO_SWC%\index.xml -xsl:%PATH_TO_SWC%\combine.xslt -o:temp\\' + variant +r'\%SWC_NAME%.xml' + end_of_line)

    merge_list.append(r'echo Merging All' + end_of_line)

    merge_list.append(r':end' + end_of_line)
    merge_list.append(r'echo -[DONE]------------------------------------------------------------------------')

    merge_file = open(merge_output_file, 'w')
    merge_file.writelines(merge_list)
    merge_file.close
