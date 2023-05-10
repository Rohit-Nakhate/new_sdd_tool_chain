@echo off

@REM Components,output_path
echo "========= Running : Get_component_path.py ========="

set "Get_component_path=get_component_path.py"
set "Input_path=D:\New_task\cloned_repo\SDD_Toolchain\sw.sys.chorus_main_doxygen_reports\mc_sw"
set "outpath=D:\New_task\cloned_repo\SDD_Toolchain\sw.tool.sdd_compliance_checker\sdd-compliance-checker"
python %Get_component_path% --input_dir %Input_path% --output_dir %outpath%

echo "========== Running : main.py =========="

set "component_list_csv=component_list.csv"
set "main=main.py"
for /f "usebackq tokens=1-2 skip=1 delims=," %%a in (%component_list_csv%) do (
	python %main% --xml-dir %%a --output-dir %%b
)
echo "========== Running : extractSDDToolchainMetrics.py =========="
set "metrics_csv=D:\New_task\cloned_repo\SDD_Toolchain\sw.tool.sdd_compliance_checker\sdd-compliance-checker"
python extractSDDToolchainMetrics.py --input_csv_file %component_list_csv% --output_csv_file %metrics_csv%
REM python csvToDB.py --xml-dir %%b --output-dir %%b\name.csv