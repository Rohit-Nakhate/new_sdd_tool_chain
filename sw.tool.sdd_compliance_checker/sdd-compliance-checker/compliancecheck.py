# Required Libraries
import appdata
import filter

################################################################################
# Function Name  : create_finding
# Arguments      : level,type,description,location
# Return Value   : finding
# Called By      : 
# Description    : 
################################################################################
def create_finding(level, type, description, location):
    file = location[0]
    line = location[1]

    finding = {
        "level": level,
        "type": type,
        "description": description,
        "file": file,
        "line": line
    }
    return finding

################################################################################
# Function Name  : check_brief_desc
# Arguments      : symbol
# Return Value   : findings
# Called By      : run_compliance_check
# Description    : 
################################################################################
def check_brief_desc(symbol):
    # check if brief description is provided
    findings = []
    if symbol is not None and filter.is_configured_check(symbol["kind"], "brief"):
        if ("brief" in symbol and not symbol['brief']) and ("detailed" in symbol and not symbol['detailed']):
            msg = "brief description missing for symbol -> " + str(symbol["symbol"] + " " + symbol["kind"])
            findings.append(create_finding("error", "brief", msg, symbol["meta"]["location"]))
    return findings

################################################################################
# Function Name  : check_enum_brief_desc
# Arguments      : symbol
# Return Value   : findings
# Called By      : run_compliance_check
# Description    : 
################################################################################
def check_enum_brief_desc(symbol):
    findings = []

    if symbol is not None and filter.is_configured_check(symbol["kind"], "enum_vars"):
        # Check if all enum vars have a brief desc
        enum_vars = symbol["enum_vars"]
        if len(enum_vars) != 0:
            for var in enum_vars:
                if var["desc"] == '':
                    msg = "enum variable" + "<" + var["name"] + ">" + " has no description"
                    findings.append(create_finding("error", "enum", msg, symbol["meta"]["location"]))

    return findings

################################################################################
# Function Name  : check_in_param_desc
# Arguments      : symbol
# Return Value   : findings
# Called By      : run_compliance_check
# Description    : 
################################################################################
def check_in_param_desc(symbol):
    findings = []

    if symbol is not None and filter.is_configured_check(symbol["kind"], "param"):
        # Check if all parameters mentioned (def = function signature)
        if len(symbol["params"]["def"]) != len(symbol["params"]["desc"]):
            create_finding("error", "param",
                           "not all input parameters described for symbol -> " + symbol["symbol"] + " " + symbol["kind"],
                           symbol["meta"]["location"])

        # Check if all mentioned parameters have description
        param_descs = symbol["params"]["desc"]
        if len(param_descs) != 0:
            for desc in param_descs:
                if desc["param_desc"] == '':
                    msg = "param " + "<" + desc["param_name"] + ">" + " has no description"
                    findings.append(create_finding("error", "param", msg, symbol["meta"]["location"]))

    return findings

################################################################################
# Function Name  : check_return_param_desc
# Arguments      : symbol
# Return Value   : findings
# Called By      : run_compliance_check
# Description    : 
################################################################################
def check_return_param_desc(symbol):
    findings = []

    if symbol is not None and filter.is_configured_check(symbol["kind"], "return"):
        # no return description required if constructor/destructor
        if symbol["return"]["type"] is "":
            return findings

        # no return description required if void
        if symbol["return"]["type"] != "void":
            # check if any descirption avaialable otherwise create finding as completly missing
            if len(symbol["return"]["desc"]) != 0:
                for val in symbol["return"]["desc"]:
                    if val["param_desc"] == '':
                        msg = "return value not described for symbol -> " + symbol["symbol"] + " " + symbol["kind"]
                        findings.append(create_finding("error", "return", msg, symbol["meta"]["location"]))
            else:
                msg = "return value not described for symbol -> " + symbol["symbol"]
                findings.append(create_finding("error", "return", msg, symbol["meta"]["location"]))

    return findings

################################################################################
# Function Name  : check_security_relevance
# Arguments      : symbol
# Return Value   : findings
# Called By      : run_compliance_check
# Description    : 
################################################################################
def check_security_relevance(symbol):
    findings = []

    if symbol is not None and filter.is_configured_check(symbol["kind"], "security"):
        # Check if spr tag is available - spr_true or spr_false
        if len(symbol["security"]) == 0:
            msg = "security rating missing for symbol -> " + symbol["symbol"] + " " + symbol["kind"]
            findings.append(create_finding("error", "security", msg, symbol["meta"]["location"]))

        # Check if justification for spr_true is available
        if len(symbol["security"]) != 0:
            for val in symbol["security"]:
                if val["security_relevance"]:
                    if val["additional_description"] == "":
                        msg = "security justification/reason missing symbol -> " + symbol["symbol"] + " " + symbol["kind"]
                        findings.append(create_finding("error", "security", msg, symbol["meta"]["location"]))

    return findings

################################################################################
# Function Name  : check_verification_criteria
# Arguments      : symbol
# Return Value   : findings
# Called By      : run_compliance_check
# Description    : 
################################################################################
def check_verification_criteria(symbol):
    findings = []

    if symbol is not None and filter.is_configured_check(symbol["kind"], "vc_info"):
        # Check if vc tag is available
        if len(symbol["test"]["vc_info"]) == 0:
            msg = "verification criteria tag (description or <N/A>) missing for symbol -> " + symbol["symbol"] + " " + \
                  symbol["kind"]
            findings.append(create_finding("error", "verification-criteria", msg, symbol["meta"]["location"]))

        # Check if testcases is linked or <N/A> via has_valid_ref (if <N/A> is provided, valid_ref is true)
        if len(symbol["test"]["vc_info"]) != 0:
            for val in symbol["test"]["vc_info"]:
                if not val["has_valid_ref"]:
                    msg = "Verification criteria not covered by test or <N/A> statement missing for symbol -> " + symbol[
                        "symbol"] + " " + symbol["kind"]
                    findings.append(create_finding("error", "security", msg, symbol["meta"]["location"]))

    return findings

################################################################################
# Function Name  : check_traceability
# Arguments      : symbol
# Return Value   : findings
# Called By      : run_compliance_check
# Description    : 
################################################################################
def check_traceability(symbol):
    findings = []

    if symbol is not None and filter.is_configured_check(symbol["kind"], "trace"):
        # Check if satify/design decision tag is available
        if len(symbol["trace"]) == 0:
            msg = "satisfy or design decision tag missing for symbol -> " + symbol["symbol"] + symbol["kind"]
            findings.append(create_finding("error", "trace", msg, symbol["meta"]["location"]))

        # Check if justification for design decision is provided
        if len(symbol["trace"]) != 0:
            for val in symbol["trace"]:
                if val["design_decision"] and val["additional_description"] == "":
                    msg = "Justification/description for design decision missing for symbol -> " + symbol["symbol"] + " " + \
                          symbol["kind"]
                    findings.append(create_finding("error", "trace", msg, symbol["meta"]["location"]))

                if val["design_decision"] and val["additional_description"] == "DeprecatedTag":
                    msg = "tag @designdecision is deprecated. Use @designdecision{justficiation} for symbol -> " + symbol[
                        "symbol"] + " " + symbol["kind"]
                    findings.append(create_finding("warning", "trace", msg, symbol["meta"]["location"]))

    return findings

################################################################################
# Function Name  : check_test_coverage
# Arguments      : symbol
# Return Value   : findings
# Called By      : run_compliance_check
# Description    : 
################################################################################
def check_test_coverage(symbol):
    # only covered if mentioned links to testcases have referece otherwise not covered
    findings = []

    if symbol is not None and filter.is_configured_check(symbol["kind"], "test"):
        # No test cases linked, check if code review tag with justification is provided, otherwise finding
        if len(symbol["test"]["test_cases"]) == 0:
            # No test case + no code review
            if len(symbol["test"]["code_review"]) == 0:
                msg = "No test cases linked or code review tag missing for symbol -> " + \
                      symbol["symbol"] + " " + symbol["kind"]
                findings.append(create_finding("error", "test", msg, symbol["meta"]["location"]))

            if len(symbol["test"]["code_review"]) != 0:
                ## check if justifiation for code review is provided
                for val in symbol["test"]["code_review"]:
                    if val["additional_description"] == "":
                        msg = "Justification for code review is missing for symbol -> " + \
                              symbol["symbol"] + " " + symbol["kind"]
                        findings.append(create_finding("error", "test", msg, symbol["meta"]["location"]))
    return findings

################################################################################
# Function Name  : run_compliance_check
# Arguments      : symbol
# Return Value   : findings
# Called By      : main
# Description    : compliance_findings, ignored_files, contains_errors
################################################################################
def run_compliance_check(symbols):
    compliance_findings = []
    ignored_files = []
    contains_errors = False

    for symbol in symbols:
        # filter files/dirs where no comliance check necessary e.g. .cpp
        if symbol["meta"]["location"] is not None:
            if not filter.is_relevant_filep(symbol["meta"]["location"][0]):
                ignored_files.append(symbol["meta"]["location"][0])
                continue

        if symbol["kind"] in ['function']:
            compliance_findings.extend(check_brief_desc(symbol))
            compliance_findings.extend(check_in_param_desc(symbol))
            compliance_findings.extend(check_return_param_desc(symbol))
            compliance_findings.extend(check_security_relevance(symbol))
            compliance_findings.extend(check_verification_criteria(symbol))
            compliance_findings.extend(check_traceability(symbol))
            compliance_findings.extend(check_test_coverage(symbol))

        elif symbol["kind"] in ['enum']:
            compliance_findings.extend(check_brief_desc(symbol))
            compliance_findings.extend(check_enum_brief_desc(symbol))

        elif symbol["kind"] == "union" or symbol["kind"] == 'struct' or symbol["kind"] == "class" or symbol["kind"] == "namespace" or symbol["kind"] == "typedef" or symbol[
            "kind"] == "define" or symbol["kind"] == "variable":
            compliance_findings.extend(check_brief_desc(symbol))

        else:
            appdata.add_limitation("undefined compliance: " + symbol["kind"])


    for finding in compliance_findings:
        if finding['level'] == 'error':
            contains_errors = True
            break

    return compliance_findings, ignored_files, contains_errors

