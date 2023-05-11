################################################################################
# This is the CSV to DB config file.
# Add list of Tables which needes to be updated.
################################################################################

# Configure the below parameters for your server & database name.
db_server_name = "192.168.1.8"
db_name = "SDD_TOOLCHAIN"


# Configure/ Add csv header names
csv_header = {
        'project_name':'project_name',
        'script_execution_time':'script_execution_time',                      
        'artifactory_upload_time':'artifactory_upload_time',                                    
        'type':'type',                                  
        'release_adaptive_version':'release_adaptive_version',                                         
        'sw_component':'sw_component', 
        'Customer':'Customer',
        'Variant':'Variant',                              
        'sw_component_rel_version':'sw_component_rel_version',                                         
        'branch':'branch',                                    
        'branch_version':'branch_version',                  
        'brief_nmb_elements':'brief_nmb_elements',                  
        'brief_nmb_not_covered':'brief_nmb_not_covered',                        
        'brief_nmb_covered':'brief_nmb_covered',                                
        'brief_pct_coverage':'brief_pct_coverage',                                 
        'enum_vars_brief_nmb_elements':'enum_vars_brief_nmb_elements',                                  
        'enum_vars_brief_nmb_not_covered':'enum_vars_brief_nmb_not_covered',                               
        'enum_vars_brief_nmb_covered':'enum_vars_brief_nmb_covered',                    
        'enum_vars_brief_pct_coverage':'enum_vars_brief_pct_coverage',                             
        'param_nmb_elements':'param_nmb_elements',
        'param_nmb_not_covered':'param_nmb_not_covered',                             
        'param_nmb_covered':'param_nmb_covered',
        'param_pct_coverage':'param_pct_coverage',                      
        'return_nmb_elements':'return_nmb_elements',                                    
        'return_nmb_not_covered':'return_nmb_not_covered',                                  
        'return_nmb_covered':'return_nmb_covered',                                         
        'return_pct_coverage':'return_pct_coverage',                                 
        'security_nmb_elements':'security_nmb_elements',                                         
        'security_nmb_not_covered':'security_nmb_not_covered',                                    
        'security_nmb_covered':'security_nmb_covered',                  
        'security_pct_coverage':'security_pct_coverage',                  
        'verification_criteria_nmb_elements':'verification_criteria_nmb_elements',                        
        'verification_criteria_nmb_not_covered':'verification_criteria_nmb_not_covered',                                
        'verification_criteria_nmb_covered':'verification_criteria_nmb_covered',                                 
        'verification_criteria_pct_coverage':'verification_criteria_pct_coverage',                                  
        'test_nmb_elements':'test_nmb_elements',                               
        'test_nmb_not_covered':'test_nmb_not_covered',                    
        'test_nmb_covered':'test_nmb_covered',                             
        'test_pct_coverage':'test_pct_coverage',
        'sdd_trace_nmb_elements':'sdd_trace_nmb_elements',                             
        'sdd_trace_nmb_not_covered':'sdd_trace_nmb_not_covered',
        'sdd_trace_nmb_covered':'sdd_trace_nmb_covered',                      
        'sdd_trace_pct_coverage':'sdd_trace_pct_coverage',                                    
        'sdd_trace_details_nmb_fcts':'sdd_trace_details_nmb_fcts',                                  
        'sdd_trace_details_nmb_dds_fct':'sdd_trace_details_nmb_dds_fct',                                         
        'sdd_trace_details_pct_dd_fct':'sdd_trace_details_pct_dd_fct',                                 
        'sdd_trace_details_nmb_req_fct':'sdd_trace_details_nmb_req_fct',                                         
        'sdd_trace_details_pct_req_fct':'sdd_trace_details_pct_req_fct',                                    
        'sdd_trace_details_nmb_linked_req_fcts':'sdd_trace_details_nmb_linked_req_fcts',                  
        'sdd_trace_details_nmb_linked_req_page':'sdd_trace_details_nmb_linked_req_page',                  
        'sdd_linked_req_ids_nmb':'sdd_linked_req_ids_nmb',                        
        'sdd_linked_req_ids_list':'sdd_linked_req_ids_list',
        'compliance_report':'compliance_report'
        }


# Configure the db_Tables parameter below with the tables and necessary queries for it.
# name    : Mention the full name of the db table.
#           db_columns : Mention the DB Columns in which you want to insert data. E.g.  [Project_ID]
#           db_values  : Mention the DB Values for above mentioned columns.       E.g.  {projectTable_projectID}
db_Tables = {
        'project' : 
        {   #please give actual table name in db for key 'name'
                'name'   : f"{db_name}.dbo.project",
                #please give name of columns for which we want to insert the values from csv into above table 
                # 'db_columns' and 'db_values' (values from the csv as per the column names)
                'insert' : {
                'db_columns' : "[project_name]",
                'db_values' : "'{csv_row[project_name]}'"
                }
        },
        'autosaar_Variant' :
        {
                'name'   : f"{db_name}.dbo.autosaar_Variant",
                'insert' : {
                'db_columns' : "[varient],[Project_id]",
                'db_values' : "'{csv_row[varient]},{Project_id}'" 
                }
        },
        'clasic_types' :
        {
                'name'   : f"{db_name}.dbo.clasic_types",
                'insert' : {
                'db_columns' : "[type],[Project_id]",
                'db_values' : "'{csv_row[type]},{Project_id}'"
                }
        },
        'clasic_sw_components' : 
        {
                'name'   : f"{db_name}.dbo.clasic_sw_components",
                'insert' : {
                'db_columns' : "[sw_component], [type_id]",
                'db_values' : "'{csv_row[sw_component]}',{type_id}"
                }
        },
        'clasic_dev_branches' : 
        {
                'name'   : f"{db_name}.dbo.clasic_dev_branches",
                'insert' : {
                'db_columns' : "[branch], [type_id]",
                'db_values' : "'{csv_row[branch]}', {type_id}"
                }
        },
        'clasic__sdd_release' :
        {
                'name'   : f"{db_name}.dbo.clasic__sdd_release",
                'insert' : {
                'db_columns' : "[release_number], [type_id]",
                'db_values' : "'{release_number}', {type_id}"
                }
        },
        'clasic_release_info':
        {
                'name' : f"{db_name}.dbo.clasic_release_info",
                'insert' :{   
                'db_columns':"[release_id],[version_id]",
                'db_values' :"{release_id},{version_id}"
                }
        },
        'clasic_sdd_compliance_checker_info' : 
        {
                'name'   : f"{db_name}.dbo.clasic_sdd_compliance_checker_info",
                'insert' : 
                {
                'db_columns' :"[script_execution_time],[artifactory_upload_time],[type_id],[sw_component_id],[customers],[variant_id],[branch_id],[version_id],[brief_nmb_elements],[brief_nmb_not_covered],[brief_nmb_covered],[brief_pct_coverage],[enum_vars_brief_nmb_elements],[enum_vars_brief_nmb_not_covered],[enum_vars_brief_nmb_covered],[enum_vars_brief_pct_coverage],[param_nmb_elements],[param_nmb_not_covered],[param_nmb_covered],[param_pct_coverage],[return_nmb_elements],[return_nmb_not_covered],[return_nmb_covered],[return_pct_coverage],[security_nmb_elements],[security_nmb_not_covered],[security_nmb_covered],[security_pct_coverage],[verification_criteria_nmb_elements],[verification_criteria_nmb_not_covered],[verification_criteria_pct_coverage],[test_nmb_elements],[test_nmb_not_covered],[test_nmb_covered],[test_pct_coverage],[sdd_trace_nmb_elements],[sdd_trace_nmb_not_covered],[sdd_trace_nmb_covered],[sdd_trace_pct_coverage],[sdd_trace_details_nmb_fcts],[sdd_trace_details_nmb_dds_fct],[sdd_trace_details_pct_dd_fct],[sdd_trace_details_nmb_req_fct],[sdd_trace_details_pct_req_fct],[sdd_trace_details_nmb_linked_req_fcts],[sdd_trace_details_nmb_linked_req_page],[sdd_linked_req_ids_nmb],[verification_criteria_nmb_covered],[compliance_report]",
                'db_values' : "'{csv_row[script_execution_time]}','{csv_row[artifactory_upload_time]}',{type_id},{sw_component_id},{branch_id},{variant_id},{branch_id},{version_id},'{csv_row[brief_nmb_elements]}','{csv_row[brief_nmb_not_covered]}','{csv_row[brief_nmb_covered]}','{csv_row[brief_pct_coverage]}','{csv_row[enum_vars_brief_nmb_elements]}','{csv_row[enum_vars_brief_nmb_not_covered]}','{csv_row[enum_vars_brief_nmb_covered]}','{csv_row[enum_vars_brief_pct_coverage]}','{csv_row[param_nmb_elements]}','{csv_row[param_nmb_not_covered]}','{csv_row[param_nmb_covered]}','{csv_row[param_pct_coverage]}','{csv_row[return_nmb_elements]}','{csv_row[return_nmb_not_covered]}','{csv_row[return_nmb_covered]}','{csv_row[return_pct_coverage]}','{csv_row[security_nmb_elements]}','{csv_row[security_nmb_not_covered]}','{csv_row[security_nmb_covered]}','{csv_row[security_pct_coverage]}','{csv_row[verification_criteria_nmb_elements]}','{csv_row[verification_criteria_nmb_not_covered]}','{csv_row[verification_criteria_pct_coverage]}','{csv_row[test_nmb_elements]}','{csv_row[test_nmb_not_covered]}','{csv_row[test_nmb_covered]}','{csv_row[test_pct_coverage]}','{csv_row[sdd_trace_nmb_elements]}','{csv_row[sdd_trace_nmb_not_covered]}','{csv_row[sdd_trace_nmb_covered]}','{csv_row[sdd_trace_pct_coverage]}','{csv_row[sdd_trace_details_nmb_fcts]}','{csv_row[sdd_trace_details_nmb_dds_fct]}','{csv_row[sdd_trace_details_pct_dd_fct]}','{csv_row[sdd_trace_details_nmb_req_fct]}','{csv_row[sdd_trace_details_pct_req_fct]}','{csv_row[sdd_trace_details_nmb_linked_req_fcts]}','{csv_row[sdd_trace_details_nmb_linked_req_page]}','{csv_row[sdd_linked_req_ids_nmb]}','{csv_row[verification_criteria_nmb_covered]}','{csv_row[compliance_report]}'"
                }
        },
        'clasic_sdd_releasesdd_linked_requirements':
        {
                'name' : f"{db_name}.dbo.clasic_sdd_releasesdd_linked_requirements",
                'insert' :
                {   
                'db_columns':"[requirements]",
                'db_values' :"'{req}'"
                }
        },
        'clasic_requirement_info':
        {   
                'name' : f"{db_name}.dbo.clasic_requirement_info",
                'insert' :
                {   
                'db_columns':"[req_id],[version_id],[branch_id],[sw_component_id]",
                'db_values' :"{req_id},{version_id},{branch_id},{sw_component_id}"
                } 
        }
}
