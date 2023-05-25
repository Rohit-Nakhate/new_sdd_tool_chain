#Required libraries
import xml.etree.ElementTree as et
from xml.dom import minidom
import filter

################################################################################
# Function Name  : create_req_xml
# Arguments      : allocated_req, meta_data
# Return Value   : pretty_xml_str
# Called By      : create_req_metric
# Description    : This function is used to create req xml
################################################################################
# TODO reduce for loops
# TODO later - check spr tag -> check if security relevant is spr true for function where spr_true requriements is linked
# TODO print list where req is covered - functions and markdown
# Used by DevOps for Grafana Dashboard
def create_req_xml(allocated_req, meta_data):
    root = et.Element("REQUIREMENTS", Component=str(meta_data["ComponentName"]), Variant=meta_data["Variant"])
    for req in allocated_req:
        et.SubElement(root, "REQUIREMENT", File=str(req[1]), Line=str(req[2]), Id=str(req[0])).text

    pretty_xml_str = minidom.parseString(et.tostring(root)).toprettyxml(indent="   ", encoding="utf-8").decode('utf-8')

    return pretty_xml_str

################################################################################
# Function Name  : create_req_metric
# Arguments      : symbols, meta_data
# Return Value   : pretty_xml_str
# Called By      : None
# Description    : This function is used to create req xml
################################################################################
# Used by DevOps for Grafana Dashboard
def create_req_metric(symbols, meta_data):
    allocated_req = []

    for symbol in symbols:
        if "trace" in symbol:
            for info in symbol["trace"]:
                if info["req_id"] != "":
                    req_list = info['req_id'].replace(';', ',').replace('\'', '').strip('.').split(',')
                    for req in req_list:
                        allocated_req.append((req, symbol["meta"]["location"][0],
                                              symbol["meta"]["location"][1]))
    return create_req_xml(allocated_req, meta_data)

################################################################################
# Function Name  : Avoid_ZeroDiv
# Arguments      : num1 , num2
# Return Value   : pretty_xml_str
# Called By      : create_req_metric
# Description    : This function is used to Avoid Zero Division
################################################################################
def Avoid_ZeroDiv(num1 , num2):
    try:
        return (num1 / num2)
    except ZeroDivisionError:
        return 0

################################################################################
# Function Name  : create_function_metric
# Arguments      : symbols, findings
# Return Value   : metrics
# Called By      : main
# Description    : This function is used to create function metric
################################################################################  
def create_function_metric(symbols, findings):
    metrics = {}

    def is_fct_metric(l_symbol):
        return filter.is_relevant_filep(l_symbol["meta"]["location"][0]) and "function" == l_symbol["kind"]

    def is_enum_metric(l_symbol):
        return filter.is_relevant_filep(l_symbol["meta"]["location"][0]) and "enum" == l_symbol["kind"]

    def is_elem_metric(l_symbol):
        return filter.is_relevant_filep(l_symbol["meta"]["location"][0]) and (l_symbol["kind"] in (
            "union", "strut", "class", "file", "namespace", "typedef", "define", "variable"))

    def is_page_metric(l_symbol):
        if l_symbol["kind"] == "page":
            return True

    # Number of functions
    nmb_fct = 0
    nmb_enums = 0
    nmb_enum_vars = 0
    nmb_other_elems = 0

    for symbol in symbols:
        if is_fct_metric(symbol):
            nmb_fct += 1

        if is_elem_metric(symbol):
            nmb_other_elems += 1

        if is_enum_metric(symbol):
            nmb_enums += 1
            if "enum_vars" in symbol:
                for e in symbol["enum_vars"]:
                    nmb_enum_vars += 1

    metrics["brief"] = get_metrics("brief", findings, nmb_fct + nmb_other_elems + nmb_enums)
    metrics["enum_vars_brief"] = get_metrics("enum", findings, nmb_enum_vars)
    metrics["param"] = get_metrics("param", findings, nmb_fct)
    metrics["return"] = get_metrics("return", findings, nmb_fct)
    metrics["security"] = get_metrics("security", findings, nmb_fct)
    metrics["verification_criteria"] = get_metrics("verification-criteria", findings, nmb_fct)
    metrics["test"] = get_metrics("test", findings, nmb_fct)
    metrics["sdd_trace"] = get_metrics("trace", findings, nmb_fct)

    #  Number of functions covered by design decision
    nmb_dd = 0
    for symbol in symbols:
        if is_fct_metric(symbol):
            if "trace" in symbol:
                for t in symbol["trace"]:
                    if t["design_decision"]:
                        nmb_dd += 1
                        break
    
    dd_ratio = round(Avoid_ZeroDiv(nmb_dd , nmb_fct) * 100, 2)

    # Number of functions covered by requirements
    nmb_req = 0
    for symbol in symbols:
        if is_fct_metric(symbol):
            if "trace" in symbol:
                for t in symbol["trace"]:
                    if not t["design_decision"]:
                        nmb_req += 1
                        break  # only count function once - when a req is found

    req_ratio = round(Avoid_ZeroDiv(nmb_req , nmb_fct) * 100, 2)

    #  Number of linked unique requirements IDs to functions
    unique_fct_ids = []
    for symbol in symbols:
        if is_fct_metric(symbol) or is_elem_metric(symbol):
            if "trace" in symbol:
                for t in symbol["trace"]:
                    if not t["design_decision"]:
                        reqs = get_req_id(t["req_id"])
                        for req in reqs:
                            if req not in unique_fct_ids:
                                unique_fct_ids.append(req)

    #  Number of linked unique requirements IDs to markdown
    unique_page_ids = []
    for symbol in symbols:
        if is_page_metric(symbol):
            if "trace" in symbol:
                for t in symbol["trace"]:
                    if not t["design_decision"]:
                        reqs = get_req_id(t["req_id"])
                        for req in reqs:
                            if req not in unique_page_ids:
                                unique_page_ids.append(req)

    trace_details = {
        "nmb_fcts": nmb_fct,
        "nmb_dd_fct": nmb_dd,  # number of functions covered by dd
        "pct_dd_fct": dd_ratio,  # ratio
        "nmb_req_fct": nmb_req,  # number of functions covered by requirements
        "pct_req_fct": req_ratio # ratio
    }

    metrics["sdd_trace_details"] = trace_details

    #  List of unique requirements id - markdown + functions
    overall_unique_ids = unique_fct_ids  # initialize with list of unique function ids

    for page_req_id in unique_page_ids:
        if page_req_id not in overall_unique_ids:
            overall_unique_ids.append(page_req_id)

    metrics["sdd_linked_req_ids"] = {
        "nmb": len(overall_unique_ids),
        "list": overall_unique_ids
    }

    return metrics

################################################################################
# Function Name  : create_function_metric
# Arguments      : symbols, findings
# Return Value   : metrics
# Called By      : create_function_metric
# Description    : This function is used to get req id
################################################################################  
def get_req_id(req_ids):
    req_list = []
    if req_ids != "":
        req_list = req_ids.replace(';', ',').replace('\'', '').strip('.').split(',')
    return req_list

################################################################################
# Function Name  : get_doors_req_metrics
# Arguments      : doors_req, sdd_metrics, target_release
# Return Value   : doors_metrics
# Called By      : main
# Description    : This function is used to get doors req metrics
################################################################################  
def get_doors_req_metrics(doors_req, sdd_metrics, target_release):
    # TODO clean up
    doors_metrics = {}

    doors_req_ids = doors_req["relevant_req"]

    if doors_req_ids:  # run if doors import was executed
        sdd_linked_req_id = sdd_metrics["sdd_linked_req_ids"]["list"]

        not_linked_doors_ids = []  # doors req which are not linked in sdd
        invalid_linked_req = []  # linked sdd req which are not valid in doors

        # check if all valid doors req are linked in sdd
        for doors_id in doors_req_ids:
            if doors_id not in sdd_linked_req_id:
                not_linked_doors_ids.append(doors_id)

        # check if sdd contains linked requirements which are not valid
        for sdd_id in sdd_linked_req_id:
            if sdd_id not in doors_req_ids:
                invalid_linked_req.append(sdd_id)

        nmb_valid_doors_req = len(doors_req_ids)

        # valid doors requirements which are linked in sdd
        nmb_valid_req_linked_sdd = len(doors_req_ids) - len(not_linked_doors_ids)

        # invalid doors requirements which are linked in sdd
        nmb_invalid_req_linked_sdd = len(invalid_linked_req)

        ratio = round((nmb_valid_req_linked_sdd / nmb_valid_doors_req) * 100, 2)

        doors_metrics["doors_sdd_trace"] = {
            "sw_release": target_release,
            "nmb_valid_doors_req": nmb_valid_doors_req,
            "nmb_valid_req_linked_in_sdd": nmb_valid_req_linked_sdd,
            "pct_coverage_valid_req": ratio,
            "nmb_invalid_req_linked_in_sdd": nmb_invalid_req_linked_sdd,
            "list_invalid_req_linked": invalid_linked_req,
            "list_not_linked_req": not_linked_doors_ids,
            "csv-available": True
        }

    else:  # provide default value for metrics
        doors_metrics["doors_sdd_cov"] = {
            "sw_release": 0,
            "nmb_valid_doors_req": 0,
            "nmb_valid_req_linked_in_sdd": 0,
            "pct_coverage_valid_req": 0,
            "nmb_invalid_req_linked_in_sdd": 0,
            "list_invalid_req_linked": 0,
            "csv-available": False
        }

    return doors_metrics

################################################################################
# Function Name  : get_metrics
# Arguments      : kind, findings, nmb_elements
# Return Value   : metric
# Called By      : create_function_metric
# Description    : This function is used to get metrics
################################################################################ 
def get_metrics(kind, findings, nmb_elements):
    nmb_not_covered = 0

    for f in findings:
        if f["type"] == kind and f["level"] == "error" and filter.is_relevant_filep(f["file"]):
            nmb_not_covered += 1

    nmb_covered = nmb_elements - nmb_not_covered

    ratio = 0.0

    if nmb_elements > 0:
        ratio = round((nmb_covered / nmb_elements) * 100, 2)
    else:
        ratio = 100.00

    metric = {
        "nmb_elements": nmb_elements,
        "nmb_not_covered": nmb_not_covered,
        "nmb_covered": nmb_covered,
        "pct_coverage": ratio
    }

    return metric
