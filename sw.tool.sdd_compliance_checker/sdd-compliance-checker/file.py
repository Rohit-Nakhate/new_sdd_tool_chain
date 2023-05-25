#Required libraries
import os
import json
import yaml

# Defining Global Parameters
separator = ";"

################################################################################
# Function Name  : create_json_dump
# Arguments      : dict_content,path,filename
# Return Value   : None
# Called By      : main
# Description    : This function is dump json data.
################################################################################
def create_json_dump(dict_content, path, filename):
    report_path = os.path.join(path, filename)
    json_content = json.dumps(dict_content, sort_keys=False, indent=4, separators=(',', ': '))
    with open(report_path, "w") as f:
        f.write(json_content)

################################################################################
# Function Name  : create_csv_finding_report
# Arguments      : findings,path,filename
# Return Value   : None
# Called By      : main
# Description    : This function is used to create csv finding report
################################################################################
def create_csv_finding_report(findings, path, filename):
    report_path = os.path.join(path, filename)

    report_file = open(report_path, 'w')
    report_file.write("level;type;description;file;line \n")

    for finding in findings:
        fd = str(
            str(finding["level"]) + separator + str(finding["type"]) + separator + str(finding["description"]) + separator + str(finding[
                "file"]) + separator + str(finding["line"]))
        report_file.write(str(fd) + '\n')

    report_file.close()

################################################################################
# Function Name  : read_yaml
# Arguments      : path,filename
# Return Value   : data
# Called By      : main
# Description    : This function is used to create csv finding report
################################################################################
def read_yaml(path, filename):
    file_path = os.path.join(path, filename)
    with open(file_path, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)

    return data

################################################################################
# Function Name  : write_list_to_file
# Arguments      : content,path,filename
# Return Value   : None
# Called By      : main
# Description    : This function is used to create csv finding report
################################################################################
def write_list_to_file(content, path, filename):
    file_path = os.path.join(path, filename)
    with open(file_path, "w") as file:
        for item in content:
            file.write("%s\n" % item)

################################################################################
# Function Name  : write_string_to_file
# Arguments      : content,path,filename
# Return Value   : None
# Called By      : main
# Description    : This function is used to create csv finding report
################################################################################
def write_string_to_file(content, path, filename):
    file_path = os.path.join(path, filename)
    with open(file_path, "w") as file:
        file.write(content)


