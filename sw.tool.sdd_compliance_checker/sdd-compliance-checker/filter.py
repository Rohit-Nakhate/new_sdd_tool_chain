# Required Libraries
import appdata


################################################################################
# Function Name  : is_relevant_filep
# Arguments      : filepath
# Return Value   : None
# Called By      : create_function_metric
# Description    : This function is dump json data.
################################################################################
def is_relevant_filep(filepath):
    # filter files/dirs where no comliance check necessary e.g. .cpp
    if filepath is not None:
        filter_dirs_excl = appdata.configuration["filter-exclude"]["directory"]
        filter_ext_excl = appdata.configuration["filter-exclude"]["filetype"]
        filter_elements_excl = filter_dirs_excl + filter_ext_excl
        filter_elements_incl = appdata.configuration["filter-include"]["filename"]

        if any(ext in filepath for ext in filter_elements_excl) and not any(ext in filepath for ext in  filter_elements_incl):
            return False
        else:
            return True

################################################################################
# Function Name  : is_configured_check
# Arguments      : symbol_kind,check_kind
# Return Value   : None
# Called By      : 
# Description    : This function is dump json data.
################################################################################
def is_configured_check(symbol_kind, check_kind):
    # complinace check configuration based on config.yaml
    configured_checks = appdata.configuration["checks"][symbol_kind]
    if configured_checks is not None and check_kind in configured_checks:
        return True
    else:
        return False
