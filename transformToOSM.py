import csv
import sys
from xml.etree.ElementTree import Element, SubElement, ElementTree


if not len(sys.argv) in [2, 3]: # if without a path of csv file to read
    print("Usage: python csvtoosm.py <csv_file> (<incoding_of_csv_file>)\n")
    sys.exit()

input_osm_file_path = sys.argv[1]
csv_file_path = sys.argv[1][:-3] + "csv"
output_osm_file_path = input_osm_file_path[:-4] + "_addr.osm"

input_csv_file = open(csv_file_path, 'r', encoding="euc-kr")
input_csv = csv.reader(input_csv_file)

input_osm_file = open(input_osm_file_path, 'r', encoding="utf-8")
input_xml = ElementTree()
input_xml.parse(input_osm_file)
root = input_xml.getroot()

for line in input_csv:
    if line[0] == "id":
        continue
    
    for way in root.iter("way"):
        if way.attrib["id"] == line[1]:
            print(line[1])
            has_addr_street = False
            has_addr_housenumber = False
            
            for tag in way.iter("tag"):
                if tag.attrib["k"] == "addr:street":
                    has_addr_street = True

            if has_addr_street:
                continue

            street_tag = SubElement(way, "tag")
            street_tag.attrib["k"] = "addr:street"
            street_tag.attrib["v"] = line[9]
            way.attrib["action"] = "modify"
            


            for tag in way.iter("tag"):
                if tag.attrib["k"] == "addr:housenumber":
                    has_addr_housenumber = True

            if has_addr_housenumber:
                continue

            housenumber_tag = SubElement(way, "tag")
            housenumber_tag.attrib["k"] = "addr:housenumber"
            housenumber_tag.attrib["v"] = line[10]

input_xml.write(output_osm_file_path)

print("Info: Writed to '" + output_osm_file_path + "'")

input_csv_file.close()
input_osm_file.close()
