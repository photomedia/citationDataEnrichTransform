from json2xml import json2xml
import json
import io
import os
import xml.etree.ElementTree as ET
import csv

path = 'enriched-publications.json'
target = 'enriched-publications.xml'
target_model='eprints-model.xml'
target_transformed= os.path.splitext(target)[0]+'-eprints-model.xml'

print ("opening: "+path)
with open(path,'r',encoding='utf-8') as jsonfile:
  jsonText = jsonfile.read()
  jsonRecords = json.loads(str(jsonText),strict=False)
  mydata=json2xml.Json2xml(jsonRecords, attr_type=False ).to_xml()
print ("opening: "+target)
myfile = open(target, "w")
myfile.write(mydata)
print ("wrote XML to: "+target)



sourcetree = ET.parse(target)
targettree = ET.parse(target_model)
sourceroot = sourcetree.getroot()
targetroot = targettree.getroot()
attrib = {}

print ("wrote XMl file.  transforming file...")
print ("source: "+target)
print ("target: "+target_transformed)

for elem in sourceroot.find("graph").findall("item"):
    #print ("found item")
    # adding an element to the root node
    targetelement = targetroot.makeelement("eprint", attrib)

    elementToAdd = elem.find('DOI')
    targetelementid = targetroot.makeelement("eprintid", attrib)
    targetelementid.text = elementToAdd.text
    targetelement.append(targetelementid)

    elementToAdd = elem.find('Year')
    targetelementid = targetroot.makeelement("date", attrib)
    targetelementid.text = elementToAdd.text
    targetelement.append(targetelementid)

    elementToAdd = elem.find('Conference')
    targetelementid = targetroot.makeelement("publication", attrib)
    targetelementid.text = elementToAdd.text
    targetelement.append(targetelementid)

    for subelem in elem.iter('concepts'):
        combinedconcepts = subelem.makeelement("concepts", attrib)
        for subsubelem in subelem.iter('item'):
            combinedconcepts.append(subsubelem)

    targetelement.append(combinedconcepts)
    targetroot.append(targetelement)
        
targettree.write(target_transformed, encoding="UTF-8")

print ("wrote result to file: "+target_transformed)
print ("done.")
