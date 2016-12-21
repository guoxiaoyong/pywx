import xmltodict

def wx_xml_parse(xml):
  try:
    xmldict = xmltodict.parse(xml)
    return xmldict['xml']
   except e:
    raise e
