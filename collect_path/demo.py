import xml.etree.ElementTree as et
# path = "D:\\python_Script\\SDD_toolchain\\sw.sys.chorus_main_doxygen_reports\\mc_sw\\cdd\\ECU_DIAG_Chorus\\BUILTINLIST\\c\\doc\\Doxygen\\xml\\md__exported_doors_specification_0_requirements.xml"
# root = et.parse(path,et.XMLParser(encoding='iso-8859-5'))
# root = next(root.iter("doxygen"))
# for i in root:
#     for j in i:
#         print(j.text)
s = {"component" : None}

print(et.tostring(s))