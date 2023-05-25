# Defining Global Parameters
parser_limitations = []
version = None
configuration = None

################################################################################
# Function Name  : add_limitation
# Arguments      : l_str
# Return Value   : None
# Called By      : run_compliance_check
# Description    : This function is used to add limitation
################################################################################
def add_limitation(l_str):
    if l_str not in parser_limitations:
        parser_limitations.append(l_str)

################################################################################
# Function Name  : get_limitation
# Arguments      : None
# Return Value   : None
# Called By      : main
# Description    : This function is used to get limitation
################################################################################
def get_limitation():
    return parser_limitations

################################################################################
# Function Name  : set_version
# Arguments      : v_str
# Return Value   : None
# Called By      : 
# Description    : This function is used to set version
################################################################################
def set_version(v_str):
    global version
    version = v_str

################################################################################
# Function Name  : set_configuration
# Arguments      : cfg_dict
# Return Value   : None
# Called By      : main
# Description    : This function is used to set configuration
################################################################################
def set_configuration(cfg_dict):
    global configuration
    configuration = cfg_dict
