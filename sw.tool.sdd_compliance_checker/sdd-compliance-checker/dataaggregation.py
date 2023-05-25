# Required Libraries
import os
import xml.etree.ElementTree as ET
import appdata
import xmlelem


class XMLProcessor:

    def __init__(self, path_xml_dir):
        self.path_xml_dir = path_xml_dir

    ################################################################################
    # Function Name  : error
    # Arguments      : err_format
    # Return Value   : None
    # Called By      : None
    # Description    : This function is used for error handling
    ################################################################################

    #  Error Handling
    @staticmethod
    def error(err_format, *args):
        try:
            msg = "ERROR - " + err_format % args
        except TypeError:
            msg = "invalid message format '%s' - args '%s'" % (err_format, str(args))

        raise RuntimeError(msg)

    ################################################################################
    # Function Name  : get_index_path
    # Arguments      : xml_dir, index_file
    # Return Value   : index_path
    # Called By      : process
    # Description    : This function is used for index file handling
    ################################################################################
    
    #  Index File Handling
    @staticmethod
    def get_index_path(xml_dir, index_file):
        index_path = os.path.join(xml_dir, index_file)

        if not os.path.exists(index_path):
            XMLProcessor.error("%s not found - %s", index_file, index_path)

        return index_path
    
    ################################################################################
    # Function Name  : get_indexed_files
    # Arguments      : self, index_content
    # Return Value   : index_files
    # Called By      : process
    # Description    : This function is used get indexed files
    ################################################################################
    def get_indexed_files(self, index_content):
        index_files = []

        for item in index_content.findall('compound'):
            kind = item.get("kind")
            refid = item.get("refid")

            if kind == "dir":
                continue

            name = refid + ".xml"
            path = os.path.join(self.path_xml_dir, name)
            # Check if path exists
            if not os.path.exists(path):
                XMLProcessor.error("could not find indexed file %s", path)

            index_files.append(path)

        return index_files
    
    ################################################################################
    # Function Name  : parse_xml_content
    # Arguments      : file_path
    # Return Value   : xml_content
    # Called By      : process
    # Description    : This function is used XML file handling
    ################################################################################

    #  XML Handling
    @staticmethod
    def parse_xml_content(file_path):
        xml_content = None
        try:
            xml_content = ET.parse(file_path,ET.XMLParser(encoding="iso-8859-5"))
            # xml_content = ET.fromstring(file_path,parser=ET.XMLParser(encoding= 'UTF-8'))
        except Exception as error:
            XMLProcessor.error("error while parsing xml file %s: %s", file_path, str(error))
        return xml_content
    
    ################################################################################
    # Function Name  : process_symbol
    # Arguments      : node
    # Return Value   : symbol
    # Called By      : process_xml_file
    # Description    : This function is used for process symbol
    ################################################################################

    @staticmethod
    def process_symbol(node):
        symbol = {}

        kind = xmlelem.get_kind(node)
        if kind == "function":
            symbol['symbol'] = xmlelem.get_name(node)
            symbol['kind'] = xmlelem.get_kind(node)
            symbol['brief'] = xmlelem.get_brief_description(node)
            symbol['detailed'] = xmlelem.get_detailed_description(node)
            symbol['meta'] = xmlelem.get_meta(node)

            symbol['return'] = xmlelem.get_return(node)
            symbol['params'] = xmlelem.get_params(node)

            symbol['globals'] = xmlelem.get_globals_info(node)

            symbol['test'] = xmlelem.get_test_info(node)
            symbol['security'] = xmlelem.get_security_info(node)
            symbol['trace'] = xmlelem.get_tracability_info(node)

        elif kind == "variable":
            symbol['symbol'] = xmlelem.get_name(node)
            symbol['kind'] = xmlelem.get_kind(node)
            symbol['brief'] = xmlelem.get_brief_description(node)
            symbol['detailed'] = xmlelem.get_detailed_description(node)
            symbol['meta'] = xmlelem.get_meta(node)

            symbol['trace'] = xmlelem.get_tracability_info(node)

            symbol['return'] = xmlelem.get_return(node)

        elif kind == "enum":
            symbol['symbol'] = xmlelem.get_name(node)
            symbol['kind'] = xmlelem.get_kind(node)
            symbol['brief'] = xmlelem.get_brief_description(node)
            symbol['meta'] = xmlelem.get_meta(node)

            symbol['enum_vars'] = xmlelem.get_enum_def_desc(node)

        elif kind == "union" or kind == 'struct' or kind == "class" or kind == "file" or kind == "namespace" or kind == "typedef" or kind == "define":
            symbol['symbol'] = xmlelem.get_name(node)
            symbol['kind'] = xmlelem.get_kind(node)
            symbol['brief'] = xmlelem.get_brief_description(node)
            symbol['meta'] = xmlelem.get_meta(node)
            symbol['trace'] = xmlelem.get_tracability_info(node)

        elif kind == "friend":
            # the real type of friend is determined in the get_kind function of the xml parser. It returns one of the
            # already covered kind e.g. function, struct..
            pass

        elif kind == "page":
            # TODO integrate in xmlelem
            # return empty list if no traceability information can be found

            file = node.find('./compoundname')
            if file is not None:
                meta = {}
                file_name = file.text + " - Markdown"
                line = 0

                meta['location'] = file_name, line
                symbol["meta"] = meta
                symbol["kind"] = "page"
                symbol['trace'] = xmlelem.get_tracability_info(node, "page")

        else:
            appdata.add_limitation("Unknown node kind: " + kind)

        if symbol is not None:
            return symbol
        
    ################################################################################
    # Function Name  : process_xml_file
    # Arguments      : self, file_path
    # Return Value   : symbols
    # Called By      : process
    # Description    : This function is used process xml files
    ################################################################################

    def process_xml_file(self, file_path):
        symbols = []
        xml_content = self.parse_xml_content(file_path)
        xml_nodes = xml_content.findall("./compounddef//memberdef")
        xml_nodes += xml_content.findall("./compounddef")

        for definition in xml_nodes:
            symbol = self.process_symbol(definition)

            if symbol:
                symbols.append(symbol)

        return symbols
    
    ################################################################################
    # Function Name  : get_metadata
    # Arguments      : self, index_page_path
    # Return Value   : meta_data
    # Called By      : process
    # Description    : This function is used get metadata
    ################################################################################

    def get_metadata(self, index_page_path):
        # TODO adapt SDD guideline and template for metadata information - clear parsability
        xml_content = self.parse_xml_content(index_page_path)
        xml_nodes = xml_content.findall("./compounddef//para//row")

        component_name = None
        variant = None

        for row in xml_nodes:
            entries = row.findall("./entry")

            if len(entries) > 1:
                entry_name = entries[0].find("para").text
                entry_content = entries[1].find("para").text

                if entry_name and entry_content:
                    if entry_name.startswith("Component"):
                        component_name = entry_content.strip()

                    if entry_name.startswith("Project"):
                        variant = entry_content.strip()

        meta_data = {
            "ComponentName": component_name,
            "Variant": variant
        }
        return meta_data
    
    ################################################################################
    # Function Name  : process
    # Arguments      : self
    # Return Value   : symbols, meta_data
    # Called By      : process_xml_file
    # Description    : This function is used process symbol and metadata
    ################################################################################
    
    def process(self):
        index_path = self.get_index_path(self.path_xml_dir, "index.xml")
        index_page_path = self.get_index_path(self.path_xml_dir, "indexpage.xml")
        xml_content = self.parse_xml_content(index_path)
        indexed_files = self.get_indexed_files(xml_content)

        symbols = []

        for fp in indexed_files:
            symbols.extend(self.process_xml_file(fp))

        meta_data = self.get_metadata(index_page_path)

        return symbols, meta_data
