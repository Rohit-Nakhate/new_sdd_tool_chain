import os
import json
import yaml

separator = ";"


def create_json_dump(dict_content, path, filename):
    report_path = os.path.join(path, filename)
    json_content = json.dumps(dict_content, sort_keys=False, indent=4, separators=(',', ': '))
    with open(report_path, "w") as f:
        f.write(json_content)


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


def read_yaml(path, filename):
    file_path = os.path.join(path, filename)
    with open(file_path, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)

    return data


def write_list_to_file(content, path, filename):
    file_path = os.path.join(path, filename)
    with open(file_path, "w") as file:
        for item in content:
            file.write("%s\n" % item)


def write_string_to_file(content, path, filename):
    file_path = os.path.join(path, filename)
    with open(file_path, "w") as file:
        file.write(content)


