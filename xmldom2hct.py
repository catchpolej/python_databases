import urllib.request
from xml.dom import minidom
xmldoc = minidom.parse(urllib.request.urlopen('http://www.hockerillct.com/2018/xml2.xml'))

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

itemlist = xmldoc.getElementsByTagName('student')   
print(len(itemlist))
print(itemlist[0].attributes['name'].value)
for s in itemlist:
    print(s.attributes['name'].value)
