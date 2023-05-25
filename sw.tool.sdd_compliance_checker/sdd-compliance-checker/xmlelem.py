# Required Libraries
import xml.etree.ElementTree as ET
import re
import appdata

################################################################################
# Function Name  : get_return
# Arguments      : node
# Return Value   : ret
# Called By      : process_symbol
# Description    : This function is used to get ret dictionary
################################################################################
def get_return(node):
    ret = {}
    ret['type'] = get_return_type(node)
    ret['desc'] = get_return_description(node)

    return ret

################################################################################
# Function Name  : get_return_type
# Arguments      : node
# Return Value   : return_type
# Called By      : get_return
# Description    : This function is used to get return type
################################################################################
def get_return_type(node):
    return_type = ""

    return_def_node = node.find("./type")
    if return_def_node is not None:
        return_def_ref_node = return_def_node.find("./ref")

        if return_def_ref_node is not None:
            return_type = return_def_ref_node.text
        else:
            if return_def_node.text is not None:
                return_type = return_def_node.text

    return return_type

################################################################################
# Function Name  : get_return_description
# Arguments      : node
# Return Value   : return_parameters
# Called By      : get_return
# Description    : This function is used to get return type
################################################################################
def get_return_description(node):
    return_parameters = []

    # get return descriptions defined as return
    return_node = node.findall('./detaileddescription/para/simplesect')

    for r_node in return_node:
        # check for @return tags
        if r_node.get("kind") == "return":
            param_desc_node = r_node.find('./para')

            param_desc = ET.tostring(param_desc_node, method='text').strip().decode("utf-8").replace("\\n", "")
            parameter_description = {
                "param_name": "",
                "param_desc": param_desc
            }

            return_parameters.append(parameter_description)

    # in case no @return found check if retval is used - located under paramlist
    if not return_parameters:
        parameter_list = node.find('./detaileddescription/para')

        if parameter_list is not None:
            for desc in parameter_list:
                param_kind = desc.get("kind")

                param_items = desc.findall("./parameteritem")
                for item in param_items:

                    if param_kind == "retval":
                        parameter_name_node = item.find('./parameternamelist')
                        param_name = "".join(parameter_name_node.itertext()).strip()

                        parameter_desc_node = item.find('./parameterdescription')

                        param_desc = "".join(parameter_desc_node.itertext()).strip()

                        parameter_description = {
                            "param_name": param_name,
                            "param_desc": param_desc
                        }
                        return_parameters.append(parameter_description)

    return return_parameters

################################################################################
# Function Name  : get_params
# Arguments      : params
# Return Value   : return_parameters
# Called By      : get_return
# Description    : This function is used to get params
################################################################################
def get_params(node):
    params = {'def': get_param_definition(node), 'desc': get_param_description(node)}

    return params

################################################################################
# Function Name  : get_param_definition
# Arguments      : node
# Return Value   : param_defs
# Called By      : get_params
# Description    : This function is used to get param definition
################################################################################
def get_param_definition(node):
    param_def_nodes = node.findall("./param")
    param_defs = []

    if param_def_nodes is not None:
        for param in param_def_nodes:
            type_node = param.find("./type")
            decl_node = param.find("./declname")
            def_node = param.find("./defname")

            type_name = ""
            decl_name = ""
            def_name = ""

            if type_node is not None:
                type_name = type_node.text

            if decl_node is not None:
                decl_name = decl_node.text

            if def_node is not None:
                def_name = def_node.text

            if type_name != "":
                param_definition = {
                    "param_decl": decl_name,
                    "param_def": def_name,
                    "param_type": type_name
                }
                param_defs.append(param_definition)

    return param_defs

################################################################################
# Function Name  : get_param_description
# Arguments      : node
# Return Value   : parameters
# Called By      : get_params
# Description    : This function is used to get param description 
################################################################################
def get_param_description(node):
    parameters = []
    parameter_list = node.find('./detaileddescription/para')

    if parameter_list is not None:
        for desc in parameter_list:
            param_kind = desc.get("kind")

            param_items = desc.findall("./parameteritem")
            for item in param_items:
                if param_kind == "param":
                    parameter_name_node = item.find('./parameternamelist')
                    param_name = "".join(parameter_name_node.itertext()).strip()

                    parameter_desc_node = item.find('./parameterdescription')

                    param_desc = "".join(parameter_desc_node.itertext()).strip()

                    parameter_description = {
                        "param_name": param_name,
                        "param_desc": param_desc,
                        "param_range": None
                    }

                    parameters.append(parameter_description)
                elif param_kind == "retval":
                    # retval is covered in get_return_description
                    pass
                else:
                    appdata.add_limitation("unknown kind of parameter: " + param_kind)

    return parameters

################################################################################
# Function Name  : get_test_info
# Arguments      : node
# Return Value   : test_info
# Called By      : process_symbol
# Description    : This function is used to get get test info
################################################################################
def get_test_info(node):
    test_info = {}
    test_info['test_cases'] = get_testmethod_info(node)
    test_info['vc_info'] = get_vc_info(node)
    test_info['code_review'] = get_code_review_info(node)

    return test_info

################################################################################
# Function Name  : get_testmethod_info
# Arguments      : node
# Return Value   : test_info
# Called By      : get_params
# Description    : This function is used to get get testmethod info
################################################################################
def get_testmethod_info(node):
    # every refence to a test case starts with "TEST_" as defined in guideline
    test_cases = []

    test_node = node.findall('./detaileddescription/para/simplesect')
    for node in test_node:
        if node.get("kind") == "par":
            title = node.find("./title")

            if title.text == "Test Method":
                linked_test_cases_nodes = node.findall("./para/ref")

                for test_case_node in linked_test_cases_nodes:
                    if test_case_node.text.startswith("TEST_"):
                        is_ref = False
                        if test_case_node.get("refid") is not None:
                            is_ref = True

                        test_link = {
                            "test_name": test_case_node.text,
                            "has_valid_ref": is_ref,
                        }
                        test_cases.append(test_link)
    return test_cases

################################################################################
# Function Name  : get_vc_info
# Arguments      : node
# Return Value   : test_cases
# Called By      : get_test_info
# Description    : This function is used to get get vc info
################################################################################
def get_vc_info(node):
    # every refence to a test case starts with "TEST_" as defined in guideline
    test_cases = []

    test_node = node.findall('./detaileddescription/para/simplesect')
    for node in test_node:
        if node.get("kind") == "par":
            title = node.find("./title")
            if title.text == "Verification Criteria":
                vc_content = node.find("./para")

                if "<N/A>" in str(vc_content.text):
                    #  indicates that no vc is requried and no test coverage
                    test_link = {
                        "test_name": "N/A",
                        "has_valid_ref": True,
                    }
                    test_cases.append(test_link)

                elif str(vc_content.text):
                    # indicated that some vc description is provided in param
                    test_link = {
                        "test_name": "Content available",
                        "has_valid_ref": True,
                    }
                    test_cases.append(test_link)

                else:
                    pass
                    # if vc_content.text is None:
                    #    vc_content_list = node.find("./para/itemizedlist/listitem/para")
                    #    print("b")
                    #    if vc_content_list.text:
                    #        test_link = {
                    #            "test_name": "VC content available",
                    #            "has_valid_ref": True,
                    #        }
                    #        test_cases.append(test_link)

                    # TODO add checking for test case links - for now disabled
                    # linked_test_cases_nodes = node.findall("./para/ref")

                    # for test_case_node in linked_test_cases_nodes:
                    #    if test_case_node.text.startswith("TEST_"):
                    #        is_ref = False
                    #        if test_case_node.get("refid") is not None:
                    #            is_ref = True

                    #        test_link = {
                    #            "test_name": test_case_node.text,
                    #            "has_valid_ref": is_ref,
                    #        }
                    #        test_cases.append(test_link)

    return test_cases

################################################################################
# Function Name  : get_code_review_info
# Arguments      : node
# Return Value   : code_review_info
# Called By      : get_test_info
# Description    : This function is used to get code review info
################################################################################
def get_code_review_info(node):
    # return empty list if no tracebilty information can be found
    code_review_info = []

    xrefsects = node.findall('./detaileddescription/para/xrefsect')
    for xrefsec in xrefsects:

        xreftitle = xrefsec.find("./xreftitle")
        xref_desc = xrefsec.findall("./xrefdescription")

        if xreftitle.text == "Code Review":
            for node in xref_desc:
                dd_node = node.findall('./para')
                for n in dd_node:
                    req_link = {
                        "code_review": True,
                        "additional_description": n.text.strip().replace("\\n", ""),
                    }

                    code_review_info.append(req_link)

    return code_review_info

################################################################################
# Function Name  : get_meta
# Arguments      : node
# Return Value   : meta
# Called By      : process_symbol
# Description    : This function is used to get meta
################################################################################
def get_meta(node):
    meta = {}
    meta['virtual'] = is_virtual(node)
    meta['const'] = is_const(node)
    meta['static'] = is_static(node)
    meta['inline'] = is_inline(node)
    meta['explicit'] = is_explicit(node)
    meta['mutable'] = is_mutable(node)
    meta['location'] = get_location(node)

    return meta

################################################################################
# Function Name  : is_mutable
# Arguments      : node
# Return Value   : None
# Called By      : get_meta
# Description    : This function is used to is mutable
################################################################################
def is_mutable(node):
    mutable = node.get("mutable")

    if mutable == "yes":
        return True
    else:
        return False

################################################################################
# Function Name  : is_mutable
# Arguments      : node
# Return Value   : None
# Called By      : get_meta
# Description    : This function is used to is virtual
################################################################################
def is_virtual(node):
    virtual = node.get("virt")

    if virtual == "virtual":
        return True
    else:
        return False

################################################################################
# Function Name  : is_mutable
# Arguments      : node
# Return Value   : None
# Called By      : get_meta
# Description    : This function is used to is const
################################################################################
def is_const(node):
    const = node.get("const")

    if const == "yes":
        return True
    else:
        return False

################################################################################
# Function Name  : is_mutable
# Arguments      : node
# Return Value   : None
# Called By      : get_meta
# Description    : This function is used to is static
################################################################################
def is_static(node):
    static = node.get("static")

    if static == "yes":
        return True
    else:
        return False

################################################################################
# Function Name  : is_inline
# Arguments      : node
# Return Value   : None
# Called By      : get_meta
# Description    : This function is used to is inline
################################################################################
def is_inline(node):
    inline = node.get("inline")

    if inline == "yes":
        return True
    else:
        return False

################################################################################
# Function Name  : is_explicit
# Arguments      : node
# Return Value   : None
# Called By      : get_meta
# Description    : This function is used to is explicit
################################################################################
def is_explicit(node):
    explicit = node.get("explicit")

    if explicit == "yes":
        return True
    else:
        return False

################################################################################
# Function Name  : get_location
# Arguments      : node
# Return Value   : None
# Called By      : get_meta
# Description    : This function is used to is get location
################################################################################
def get_location(node):
    location = node.find('./location')

    if location is not None:
        file = location.get("file")
        line = location.get("line", 1)

        if (file is None) or (line is None):
            print("unable to get location from node %s", ET.tostring(node))

        return file, line
    else:
        return None

################################################################################
# Function Name  : get_kind
# Arguments      : node
# Return Value   : node_kind
# Called By      : process_symbol
# Description    : This function is used to is get kind
################################################################################
def get_kind(node):
    node_kind = node.get("kind")

    if node_kind == 'friend':
        is_definition = (node.get('inline') == 'yes' or node.find('initializer') is not None)

        if is_definition:
            friend_type_node = node.find('type')

            if friend_type_node is not None:
                friend_type = friend_type_node.text
                if friend_type == 'friend class':
                    node_kind = 'class'
                elif friend_type == 'friend struct':
                    node_kind = 'struct'
                elif friend_type == 'friend union':
                    node_kind = 'union'
                else:
                    node_kind = 'function'
    return node_kind

################################################################################
# Function Name  : get_name
# Arguments      : node
# Return Value   : node_kind
# Called By      : process_symbol
# Description    : This function is used to is get name
################################################################################
def get_name(node):
    n_id = node.get("id")
    definition = node.find("./definition")
    name = node.find("./name")
    compound_name = node.find("./compoundname")

    member_name = None

    if definition is not None:
        member_name = definition.text
    elif name is not None:
        member_name = name.text
    elif compound_name is not None:
        member_name = compound_name.text
    elif n_id is not None:
        member_name = n_id

    argsstr = node.find("./argsstring")
    arguments = ""
    if argsstr is not None:
        if argsstr.text:
            arguments = argsstr.text

    return member_name + " - " + arguments

################################################################################
# Function Name  : get_brief_description
# Arguments      : node
# Return Value   : brief_desc
# Called By      : process_symbol
# Description    : This function is used to get brief description
################################################################################
def get_brief_description(node):
    brief_desc_node = node.find("./briefdescription")
    brief_desc = "".join(brief_desc_node.itertext()).strip()

    return brief_desc

################################################################################
# Function Name  : get_brief_description
# Arguments      : node
# Return Value   : brief_desc
# Called By      : process_symbol
# Description    : This function is used to get brief description
################################################################################
def get_detailed_description(node):
    detailed_desc_node = node.find('./detaileddescription/para')
    detailed_desc = None
    if detailed_desc_node is not None:
        detailed_desc = detailed_desc_node.text
    else:
        detailed_desc = None

    return detailed_desc

################################################################################
# Function Name  : get_enum_def_desc
# Arguments      : node
# Return Value   : enum_vars
# Called By      : process_symbol
# Description    : This function is used to get enum def desc
################################################################################
def get_enum_def_desc(node):
    enum_name = node.find("./name")
    enum_vars = []

    if enum_name is not "":
        enum_var_nodes = node.findall("./enumvalue")

        if enum_var_nodes is not None:

            for enum in enum_var_nodes:
                enum_var_name = enum.find("./name")
                enum_var_brief_desc = enum.find("./briefdescription/para")

                enum_definition = {}

                if enum_var_name is not None:
                    enum_definition["name"] = enum_var_name.text
                else:
                    enum_definition["name"] = ""

                if enum_var_brief_desc is not None:
                    enum_definition["desc"] = enum_var_brief_desc.text
                else:
                    enum_definition["desc"] = ""

                enum_vars.append(enum_definition)

    return enum_vars

################################################################################
# Function Name  : get_security_info
# Arguments      : node
# Return Value   : security_info
# Called By      : process_symbol
# Description    : This function is used to get security info
################################################################################
def get_security_info(node):
    # return empty list if no tracebilty information can be found
    security_info = []

    xrefsects = node.findall('./detaileddescription/para/xrefsect')
    for xrefsec in xrefsects:

        xreftitle = xrefsec.find("./xreftitle")
        xref_desc = xrefsec.findall("./xrefdescription")

        # SPR_TURE
        if xreftitle.text == "Security Relevance":
            for node in xref_desc:
                dd_node = node.find('./para')

                node_str = str(ET.tostring(dd_node, method='text').strip()).replace("\\n", "")
                split_para = node_str.split(" Reason:")

                sec_info = {
                    "security_relevance": True,
                    "additional_description": split_para[1].strip(),
                }

                security_info.append(sec_info)

    # SPR FALSE CASE
    sec_node = node.findall('./detaileddescription/para/simplesect')
    for node in sec_node:
        if node.get("kind") == "par":
            title = node.find("./title")
            if title.text.strip() == "Security Relevance":
                sec_info = {
                    "security_relevance": False,
                    "additional_description": ""
                }
                security_info.append(sec_info)

    return security_info

################################################################################
# Function Name  : parse_traceabily_section
# Arguments      : node, xrefsects
# Return Value   : linked_requirements
# Called By      : get_tracability_info
# Description    : This function is used to parse traceabily section
################################################################################
def parse_traceabily_section(node, xrefsects):
    linked_requirements = []
    for xrefsec in xrefsects:

        xreftitle = xrefsec.find("./xreftitle")
        xref_desc = xrefsec.findall("./xrefdescription")

        if xreftitle.text == "Satisfies requirement":

            for node in xref_desc:
                req_links_node = node.findall('./para')

                for n in req_links_node:
                    node_str = str(ET.tostring(n, method='text').strip()).replace("\\n", "")

                    prefix = appdata.configuration["requirements"]["prefix"]
                    regex = "(" + prefix + "[^\s]+)"
                    split_para = re.split(regex, node_str)

                    if len(split_para) > 1:
                        clean_quot = split_para[1].strip('\'')
                        clean_white = clean_quot.strip()

                        req_link = {
                            "req_id": clean_white,
                            "additional_description": "",
                            "design_decision": False
                        }
                        if len(split_para) > 2:
                            req_link["additional_description"] = split_para[2].strip()

                        linked_requirements.append(req_link)

        if xreftitle.text == "Design Decision":
            for node in xref_desc:
                dd_node = node.findall('./para')
                for n in dd_node:
                    req_link = {
                        "req_id": "",
                        "additional_description": n.text.strip().replace("\\n", ""),
                        "design_decision": True
                    }

                    linked_requirements.append(req_link)

    detailed_desc_node = node.findall('./detaileddescription/para')
    for n in detailed_desc_node:
        detailed_desc_line = ET.tostring(n, method='text')

        if "Design Decision" in str(detailed_desc_line):
            req_link = {
                "req_id": "",
                "additional_description": "DeprecatedTag",
                "design_decision": True
            }
            linked_requirements.append(req_link)

    return linked_requirements

################################################################################
# Function Name  : get_tracability_info
# Arguments      : node, type
# Return Value   : linked_requirements
# Called By      : process_symbol
# Description    : This function is used to parse traceabily info
################################################################################
def get_tracability_info(node, type="header"):
    # type = "markdown" -> parse satisfy link from markdown
    # type = "header" -> parse satisfy link from header - default
    # return empty list if no traceability information can be found
    linked_requirements = []

    if type == "page":
        sections = node.findall('./detaileddescription/sect1')

        for s in sections:
            xrefsects = s.findall('./para/xrefsect')
            linked_requirements.extend(parse_traceabily_section(node, xrefsects))

    if type == "header":
        xrefsects = node.findall('./detaileddescription/para/xrefsect')
        linked_requirements = parse_traceabily_section(node, xrefsects)

    return linked_requirements

################################################################################
# Function Name  : get_globals_info
# Arguments      : node
# Return Value   : globals_info
# Called By      : process_symbol
# Description    : This function is used to get globals info
################################################################################
def get_globals_info(node):
    # return empty list if no global information can be found
    globals_info = []

    global_node = node.findall('./detaileddescription/para/simplesect')

    for node in global_node:
        if node.get("kind") == "par":
            title = node.find("./title")

            if title.text == "Globals":
                global_content = node.find("./para")
                if global_content.text:
                    info = {
                        "additional_description": global_content.text.strip()
                    }
                    globals_info.append(info)

    return globals_info
