import csv
import sys
from xml.etree.ElementTree import Element, SubElement, ElementTree

#osm_file_path = sys.argv[1]
#csv_file_path = osm_file_path[:-3] + "csv"

#if not len(sys.argv) == 2: # if without a path of csv file to read
#    print("Usage: python transformToCSV.py <osm_file>\n")
#    sys.exit()

osm_file_path = "sinchang4.osm"
csv_file_path = osm_file_path[:-3] + "csv"
input_osm = open(osm_file_path, 'r', encoding="utf-8")
output = open(csv_file_path,'w', newline='')
output_csv = csv.writer(output)
output_csv.writerow(["id", "version", "lat", "lon"])

input_xml = ElementTree()
input_xml.parse(input_osm)
root = input_xml.getroot()

for way in root.iter("way"):
    is_building = False
    
    for tag in way.iter("tag"):
        if tag.attrib["k"] == "building":
            is_building = True
            break

    if not is_building:
        continue

    nodes_ref = way.findall("nd")

    count_nodes = 0
    sum_coord = [0, 0]
    for ref in nodes_ref:
        exist_ref = False # existance of the node which has the reference
        
        for node in root.iter("node"):
            if node.attrib["id"] == str(ref.attrib["ref"]):
                sum_coord[0] += float(node.attrib["lat"])
                sum_coord[1] += float(node.attrib["lon"])
                exist_ref = True
                count_nodes += 1
                break

        if not exist_ref:
            print("Error: It's do not exist of the node which has the follow id in a building data: " + str(ref.attrib["ref"]))
            sys.exit()

    # print(sum_coord)
    output_csv.writerow([way.attrib["id"], way.attrib["version"],
                         round(sum_coord[0] / count_nodes, 7),
                         round(sum_coord[1] / count_nodes, 7)])

input_osm.close()
output.close()

print("Info: Writed to '" + csv_file_path + "'")
