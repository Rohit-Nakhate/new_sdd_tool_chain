#! usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
# This script is used to generate metrics json
# Usage : python extractSDDMetrics.py
#          --xml-dir =<INPUT DIR> 
#          --output-dir=<OUTPUT DIR>
# Based on different scenario script will return exit code as follows:
#  -1: Script Failure.
################################################################################

#Required libraries
import argparse
import os
import sys
from argparse import RawTextHelpFormatter
import dataaggregation
import compliancecheck
import metrics
import appdata
import file
import doorsimport


################################################################################
# Function Name  : main
# Arguments      : None
# Return Value   : 0,-1
# Called By      : None
# Description    : This is the main function.
################################################################################

def main():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, prog="sdd-compliance-metrics-checker")

    required_args = parser.add_argument_group("required")
    optional_args = parser.add_argument_group("optional")

    required_args.add_argument("--xml-dir",
                               action="store",
                               help="path to generated doxygen xml directory",
                               required=True)
    required_args.add_argument("--output-dir",
                               action="store",
                               help="path to output directory",
                               required=True)

    optional_args.add_argument("--doors-csv",
                               action="store",
                               help="path to doors csv export with requirements",
                               required=False)

    optional_args.add_argument("--target-release",
                               action="store",
                               help="target software release as integer (no leading zero), e.g. 170",
                               required=False)

    args = parser.parse_args()
    output = args.output_dir
    # Check if output exist 
    if not os.path.exists(output):
        os.makedirs(output)

    print("---- SDD Compliance Check - Start ----")
    print("Running with args: \n" + str(args))

    if args.doors_csv and not args.target_release:
        print("Error Args - Doors csv or target release missing.")
        return
    
    # Load Configuration
    appdata.set_configuration(file.read_yaml(os.path.join(os.getcwd(),""), "config.yaml"))
    #appdata.set_configuration(file.read_yaml("", "config.yaml"))
    print("\nCC Configuration: \n" + str(appdata.configuration) + "\n")

    # Parse XML
    print("Parsing xml...")
    xml_data = dataaggregation.XMLProcessor(args.xml_dir)
    syms, meta_data = xml_data.process()

    # Run Compliance Check
    print("Running compliance check...")
    findings, ignored_files, contains_errors = compliancecheck.run_compliance_check(syms)

    # Debug Files
    print("Creating debug files...")
    file.create_json_dump(syms, args.output_dir, "parser_output.json")
    file.write_list_to_file(ignored_files, args.output_dir, "ignored-files.txt")

    # Reports
    print("Creating reports...")
    file.create_json_dump(findings, args.output_dir, "sdd-compliance-report.json")
    file.create_csv_finding_report(findings, args.output_dir, "sdd-compliance-report.csv")

    # Metrics
    print("Creating metrics...")
    req_xml_str = metrics.create_req_metric(syms, meta_data)
    file.write_string_to_file(req_xml_str, args.output_dir, "requirments-allocation.xml")

    _metrics = {}

    sdd_metrics = metrics.create_function_metric(syms, findings)
    _metrics.update(sdd_metrics)

    if args.doors_csv and args.target_release:  # only run import if arg and target release is provided
        relevant_doors_req_id = {}
        relevant_doors_req_id = doorsimport.get_req_ids(args.doors_csv, int(args.target_release))
        doors_metrics = metrics.get_doors_req_metrics(relevant_doors_req_id, sdd_metrics, int(args.target_release))
        _metrics.update(doors_metrics)

    file.create_json_dump(_metrics, args.output_dir, "metrics.json")

    print("\nFindings will level error detected?", str(contains_errors))

    print("\nCC Known Limitations: \n" + str(appdata.get_limitation()))
    print("---- SDD Compliance Check - End ----")

    if contains_errors:
        # return code 2 in case of findings with level error are detected - used for jenkins pipeline failure
        sys.exit(2)


if __name__ == "__main__":
    main()
