import json
import csv
import traceback
import random

# Fixes the main ufo_awesome dataset for json Formatting errors
def fixJSONFormat(input_file, output_file):
    json_array = json.loads("[]")
    with open(input_file, 'r', encoding="utf-8") as json_string:
        line_count = 0
        for line in json_string:
            line_count += 1
            try:
                line = line.replace('\'', '-')
                json_line = json.loads(line)
                json_array.append(json_line)
            except ValueError:
                print("\n Line No. " + str(line_count) + " has JSON error")

    with open(output_file, "w", encoding="utf-8") as text_file:
        json_array = str(json_array).replace('\'', '\"')
        #text_file.write(str(json_array))
        text_file.write(json.dumps(json.loads(json_array), indent=4))


# Pretty prints JSON files
def prettyPrintJSON(input_file, output_file):

    with open(input_file, 'r', encoding="utf-8") as infile:
        data = infile.read()
        with open(output_file, 'w') as outfile:
            outfile.write(json.dumps(json.loads(data), indent=4))

# Tests if JSON file is correctly formatted
def testFileJsonLoadable(input_file):
    try:
        infile = open(input_file, 'r', encoding="utf-8")
        data = infile.read()
        json_array = json.loads(data)
    except:
        traceback.print_exc()

# Adds latitude and longitude to air pollution dataset
def match_air_location():
    infile = open('data_files/uscities.json', 'r', encoding="utf-8")
    data = infile.read()
    cities_json_array = json.loads(data)


    infile = open('data_files/reduced_air_pollution.json', 'r', encoding="utf-8")
    data = infile.read()
    air_json_array = json.loads(data)


    count = 0
    item_entry = 0;
    for item in air_json_array:
        item_entry = item_entry + 1
        try:
            for item2 in cities_json_array:
                if item["City"] == item2["city_ascii"]:
                    count += 1
                    item["latitude"] = item2["lat"]
                    item["longitude"] = item2["lng"]
                    break
        except:
            print("Error " + str(item_entry))
    print(count)
    with open('data_files/dummy.json', 'w') as outfile:
        air_json_array = str(air_json_array).replace('\'', '\"')
        outfile.write(json.dumps(json.loads(air_json_array), indent=4))

# Adds latitude and longitude to ufo dataset
def match_ufo_location():
    infile = open('data_files/uscities.json', 'r', encoding="utf-8")
    data = infile.read()
    cities_json_array = json.loads(data)
    cities_json_array = cities_json_array

    infile = open('data_files/fixed_ufo_awesome.json', 'r', encoding="utf-8")
    data = infile.read()
    ufo_json_array = json.loads(data)
    ufo_json_array = ufo_json_array

    info_string = ""

    count = 0
    item_entry = 0
    for item in ufo_json_array:
        item_entry = item_entry + 1
        try:
            for item2 in cities_json_array:
                if item2["city_ascii"] in item["location"]:
                    count += 1
                    item["latitude"] = item2["lat"]
                    item["longitude"] = item2["lng"]
                    break
        except:
            info_string += "\nError " + str(item_entry)
    info_string += "\n Count of entries processed: " + str(count)
    with open('data_files/dummy.json', 'w') as outfile:
        ufo_json_array = str(ufo_json_array).replace('\'', '\"')
        outfile.write(json.dumps(json.loads(ufo_json_array), indent=4))

    with open('data_files/info.json', 'w') as outfile:
        outfile.write(info_string)

def getCountOfEntriesOfJson(input_file):
    infile = open(input_file, 'r', encoding="utf-8")
    data = infile.read()
    json_array = json.loads(data)
    #print(len(json_array['result']))
    print(len(json_array))


# Reduces json file by randomly picking entries
def reduce_json_file(input_file, output_file):
    infile = open(input_file, 'r', encoding="utf-8")
    data = infile.read()
    json_array = json.loads(data)
    new_json_array = json.loads("[]")

    errCount = 0
    for x in range(1000):
        index = random.randint(1, 60000)
        if(is_json(str(json_array[index]).replace('\'', '\"'))):
            json_array[index].pop('description', None)
            new_json_array.append(json_array[index])
        else:
            #print(json_array[index])
            errCount += 1
    print("\nErrCount " + str(errCount))

    with open(output_file, 'w') as outfile:
        new_json_array = str(new_json_array).replace('\'', '\"')
        outfile.write(json.dumps(json.loads(new_json_array), indent=4))
        #outfile.write(str(new_json_array))


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except:
        return False
    return True

def convertCsvToJson(csv_file, json_file):

    # Open the CSV
    input_file = open(csv_file, 'rU', encoding="utf-8")
    reader = csv.reader(input_file) #added for fetching header row
    header_row = next(reader) #added for fetching header row
    reader = csv.DictReader(input_file, fieldnames=header_row)
    # Parse the CSV into JSON
    json_string = json.dumps([row for row in reader], indent=4)
    with open(json_file, 'w') as outfile:
        outfile.write(json_string)

# Counts no. of entries with lat/long
def getCountOfLoc(input_file):
    infile = open(input_file, 'r', encoding="utf-8")
    data = infile.read()
    json_array = json.loads(data)

    loc_count = 0
    for item in json_array:
        if 'latitude' in item:
            loc_count += 1

    print(loc_count)

########################################################################################################
#                MAIN MODULE
########################################################################################################

#fixJSONFormat('data_files/ufo_awesome.json', 'data_files/fixed_ufo_awesome.json')
#testFileJsonLoadable('data_files/twitter.json')
#convertCsvToJson('data_files/ufo_with_latlong.csv', 'data_files/ufo_with_latlong.json')
#testFileJsonLoadable('data_files/2pprint.json')
#testFileJsonLoadable('data_files/ufo_awesome_withlatlong_result1.json')
#prettyPrintJSON('data_files/ufo_awesome_withlatlong_result1.json', 'data_files/prettyPrinted.json')
#match_air_location()
#match_ufo_location()
#testFileJsonLoadable('data_files/reduced_final.json')
#getCountOfEntriesOfJson('data_files/reduced_air_pollution.json')
reduce_json_file('data_files/final.json', 'data_files/reduced_final.json')
#getCountOfLoc('data_files/air_poll_lat_long.json')
#testFileJsonLoadable('data_files/ufo_awesome_test.json')
pass