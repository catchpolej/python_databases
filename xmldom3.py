import urllib.request
from xml.dom import minidom
xmldoc = minidom.parse('xml3.xml')

def findChildNodeByName(parent, name):
    for node in parent.childNodes:
        if node.nodeType == node.ELEMENT_NODE and node.localName == name:
            return node
    return None

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

pagelist = xmldoc.getElementsByTagName('page')
print(len(pagelist))

for s in pagelist:
    print(s.attributes['category'].value)
    purpose = findChildNodeByName(s, 'purpose')
    if purpose is not None:
        print (getText(purpose.childNodes))
