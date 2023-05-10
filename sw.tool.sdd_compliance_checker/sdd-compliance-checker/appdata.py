parser_limitations = []
version = None
configuration = None


def add_limitation(l_str):
    if l_str not in parser_limitations:
        parser_limitations.append(l_str)


def get_limitation():
    return parser_limitations


def set_version(v_str):
    global version
    version = v_str


def set_configuration(cfg_dict):
    global configuration
    configuration = cfg_dict
