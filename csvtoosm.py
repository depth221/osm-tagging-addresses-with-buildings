import csv
import sys
from xml.etree.ElementTree import Element, SubElement, ElementTree

csv_file_path = sys.argv[1]
osm_file_path = sys.argv[1][:-3] + "osm"

if not len(sys.argv) in [2, 3]: # if without a path of csv file to read
    print("Usage: python csvtoosm.py <csv_file> (<incoding_of_csv_file>)\n")
    sys.exit()

csv_incoding = "utf-8" # set the incoding of csv file to read
if len(sys.argv) == 3:
    csv_incoding = sys.argv[2]
print("Info: Incoding of the csv file is " + csv_incoding)

fr = open(csv_file_path, 'r', encoding=csv_incoding)

fr_csv_r = csv.reader(fr);
fr_csv = []
for line in fr_csv_r: # convert the csv object to a list
    fr_csv.append(line)

fw_xml = Element('osm') # root of osm file
fw_xml.attrib['version'] = '0.6'
fw_xml.attrib['generator'] = 'JOSM'

keys_to_add = fr_csv[0]

for i in range(1, len(fr_csv)):
    node = SubElement(fw_xml, 'node') # add each node
    node.attrib['id'] = str(-200000 - i)
    node.attrib['action'] = 'modify'
    node.attrib['visible'] = 'true'

    if not fr_csv[i][0] or not fr_csv[i][1]:
        print("Error: All of lines must have coordinate")
        sys.exit()
    else:    
        node.attrib['lat'] = fr_csv[i][0]
        node.attrib['lon'] = fr_csv[i][1]

    for j in range(2, len(keys_to_add)): # add tags
        if fr_csv[i][j]:
            tag = SubElement(node, 'tag')
            tag.attrib['k'] = keys_to_add[j]
            tag.attrib['v'] = fr_csv[i][j]

tree = ElementTree(fw_xml)
print("Info: Done building the tree")
try:
    tree.write(osm_file_path, encoding = "utf-8", xml_declaration = True) # write
except:
    print("Error: Please delete '" + osm_file_path + "'")
    sys.exit()
    
print("Info: Writed to '" + osm_file_path + "'")

fr.close()
