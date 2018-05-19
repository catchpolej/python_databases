import urllib.request
from xml.dom import minidom
xmldoc = minidom.parse('xml2.xml')

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

itemlist = xmldoc.getElementsByTagName('item')
print(len(itemlist))
print(itemlist[0].attributes['name'].value)
for s in itemlist:
    print(s.attributes['name'].value)

itemlist = xmldoc.getElementsByTagName('teacher')
print(len(itemlist))
print(itemlist[0].attributes['name'].value)
for s in itemlist:
    print("Teacher",s.attributes['name'].value,"age: ",s.getAttribute("age"))
    age = findChildNodeByName(s, 'age')
    if age is not None:
        print (getText(age.childNodes))

itemlist = xmldoc.getElementsByTagName('student')   
print(len(itemlist))
print(itemlist[0].attributes['name'].value)
for s in itemlist:
    print(s.attributes['name'].value)
