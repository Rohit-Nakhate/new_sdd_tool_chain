@echo off

@REM Extracting Components,output_path
echo "========= Running : Get_component_path.py ========="

set "Get_component_path=get_component_path.py"
set "Input_path=D:\New_task\cloned_repo\GIT_CLONE\new_sdd_tool_chain\sw.sys.chorus_main_doxygen_reports\mc_sw"
set "output_path=D:\New_task\cloned_repo\GIT_CLONE\new_sdd_tool_chain\sw.sys.chorus_main_doxygen_reports\output"
python %Get_component_path% --input_dir %Input_path% --output_dir %output_path%

@ REM Generateing metrics.json For Components
echo "========== Running : main.py =========="

set "component_list_csv=component_list.csv"
set "main=main.py"
for /f "usebackq tokens=1-2 skip=1 delims=," %%a in (%component_list_csv%) do (
	python %main% --xml-dir %%a --output-dir %%b
)

@ REM Generateing SDD Tool Chain Metrics CSV File 
echo "========== Running : extractSDDToolchainMetrics.py =========="

set "extract_SDD_Metrics=extractSDDToolchainMetrics.py"
REM set component_list_csv = "D:\New_task\cloned_repo\GIT_CLONE\new_sdd_tool_chain\sw.tool.sdd_compliance_checker\sdd-compliance-checker\component_list.csv"
set "metrics_csv=D:\New_task\cloned_repo\GIT_CLONE\new_sdd_tool_chain\sw.tool.sdd_compliance_checker\sdd-compliance-checker\Review\metrics.csv"
python %extract_SDD_Metrics% --input_csv_file %component_list_csv% --output_csv_file %metrics_csv%


@ REM Executing CSV To DB Script
echo "========== Running : extractSDDToolchainCSV_TO_DB.py =========="

set "CSV_TO_DB=extractSDDToolchainCSV_TO_DB.py"
set "metrics_csv=D:\New_task\cloned_repo\GIT_CLONE\new_sdd_tool_chain\sw.tool.sdd_compliance_checker\sdd-compliance-checker\Review\metrics.csv"
set	"db_user_name=%1"
set "db_password=%2"
python %CSV_TO_DB%  --db_user_name %db_user_name% --db_password %db_password% --input_csv_file %metrics_csv%
 
echo "============== Batch File Run Sucessfully ================"