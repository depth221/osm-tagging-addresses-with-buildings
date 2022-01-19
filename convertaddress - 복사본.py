import csv
import sys
import re
import time

start = time.time()

csv_file_path = "jj3_shp.csv"

csv_incoding = "euc-kr" # set the incoding of csv file to read
if len(sys.argv) == 3:
    csv_incoding = sys.argv[2]
print("Info: Incoding of the csv file is " + csv_incoding)

fr = open(csv_file_path, 'r', encoding=csv_incoding)

fr_csv_r = csv.reader(fr);
fr_csv = []
for line in fr_csv_r: # convert the csv object to a list
    fr_csv.append(line)

keys_to_add = fr_csv[0]

fr_csv[0].append('addr:district')
fr_csv[0].append('addr:street')
fr_csv[0].append('addr:housenumber')
fr_csv[0].append('addr:subdistrict')
fr_csv[0].append('addr:unit')
fr_csv[0].append('level')
fr_csv[0].append('addr:door')

for j in range(2, len(keys_to_add)):
    if keys_to_add[j] in ['도로명주소', 'addr:full']:
        # if addresses exist
        print("Info: Found the tag '" + keys_to_add[j] + "'")
        
        for i in range(1, len(fr_csv)):
            print(i)
            province = ""
            is_exception = False # cannot be automatically converted
            
            if fr_csv[i][j]: # if the address exists
                address_splitted = fr_csv[i][j].replace("(", " (").split()
                fr_csv[i].extend([None] * 7)
                for factor in address_splitted:
                    # print(factor)
                    
                    if factor[0] == "(": # erase ()
                        factor = factor[1:]
                    if factor[-1] == ")":
                        factor = factor[:-1]

                    if len(factor) == 0:
                        continue
                    
                    if factor[-1] == "도": # addr:province
                        province = "do"
                    
                    elif len(factor) >= 3 and factor[-3:] in ["특별시", "광역시", "자치시"]: # addr:province
                        if factor[-3:] == "특별시":
                            province = "teuk"
                        elif factor[-3:] == "광역시":
                            province = "gwang"
                        elif factor[-3:] == "자치시":
                            province = "jachi"

                    elif factor[-1] in ["시", "군", "구"]:
                        if province in ["teuk", "gwang", "jachi"]:
                           fr_csv[i][-7] == factor # addr:district
                        # else:
                            # addr:city
                    
                    elif len(factor) >= 2 and factor[-2].upper() == factor[-2].lower() and factor[-1] in ["읍", "면", "동"]:
                        if (len(factor) >= 3 and not factor[-3:-2].isdecimal()) or\
                                (len(factor) == 2 and not factor[-2].isdecimal()):
                            if fr_csv[i][-4]:
                                fr_csv[i][-3] = factor[:-1] # addr:unit (exception)
                                is_exception = True
                            else:
                                fr_csv[i][-4] = factor
                    elif len(factor) >= 3 and factor[-3] == "로" and factor[-2].isdecimal() and factor[-1] == "가":
                        fr_csv[i][-4] = factor # addr:subdistrict
                    elif (len(factor) >= 4 and\
                             len(re.findall("\d", factor)) <= 1 and\
                             factor[0] == "(" and factor[-1] == ")" and\
                             factor[-3].upper() == factor[-3].lower() and\
                             factor[-2] in ["읍", "면", "동", "가"])\
                        or len(factor) >= 5 and\
                             factor[-3].isdecimal() and\
                             factor[0] == "(" and factor[-1] == ")" and\
                             factor[-2] == "가": 
                        # 1. avoid out of range error
                        # 2. only has one digit
                        fr_csv[i][-4] = factor[1:-1] # (OOn-dong)

                    elif factor[-1] in ["로", "길"]: # addr:street
                        if fr_csv[i][-6]:
                            is_exception = True
                        else:
                            fr_csv[i][-6] = factor
                        
                    elif factor.replace('-', '').replace(',', '').isdecimal(): # addr:housenumber
                        if fr_csv[i][-5]:
                            is_exception = True
                            continue
                            
                        if factor[-1] == ",":
                            fr_csv[i][-5] = factor[:-1]
                        else:
                            fr_csv[i][-5] = factor

                    elif (len(factor) >= 2 and factor[-1] == "동"):
                        if factor[:-1].isdecimal() or factor[-2].upper() != factor[-2].lower():
                            if fr_csv[i][-3]:
                                fr_csv[i][-4] = factor # addr:subdistrict (exception)
                                is_exception = True
                            else:
                                fr_csv[i][-3] = factor[:-1] # addr:unit

                    elif (len(factor) >= 2 and factor[-1] == "호"):
                        if fr_csv[i][-1]:
                            is_exception = True
                        else:
                            fr_csv[i][-1] = factor[:-1].replace('~', '-') # addr:room            

                    elif factor[-1] == "층": # level
                        if factor[0:2] == "지하":
                            fr_csv[i][-2] = "-" + factor[2:-1] # basement
                        elif factor[0] == "B":
                            fr_csv[i][-2] = "-" + factor[1:-1] # basement
                        elif factor[:-1].isdecimal():
                            fr_csv[i][-2] = factor[:-1]
                        else:
                            is_exception = True

                    else:
                        is_exception = True

                if not is_exception:
                    fr_csv[i][j] = ""

print("Info: Done converting")
fr.close()
try:
    fw = open(csv_file_path[:-4] + "_address.csv", 'w', encoding=csv_incoding, newline='') # write
except:
    print("Error: Please delete '" + csv_file_path[:-4] + "_address.csv (%.3fs)" %(time.time() - start))
    sys.exit()

writer = csv.writer(fw)
for i in fr_csv:
    writer.writerow(i)

print("Info: Writed to '" + csv_file_path[:-4] + "_address.csv' (%.3fs)" %(time.time() - start))
fw.close()
