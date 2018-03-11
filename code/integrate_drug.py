__author__ = 'weiweiduan'
import json
import sys

# drug = open("drug_poisoning.csv", "r")
drug = open(sys.argv[1], "r")
drug_data = []
count = 0
for line in drug:
    if count == 0:
        count += 1
        continue
    tmpt = line.strip().split(",")
    drug_data.append(tmpt)

# with open('uscities.json') as data_file:
with open(sys.argv[2]) as data_file:
    city_data = json.loads(data_file.read())

# with open('disease_ufo_2014.json') as data_file:
with open(sys.argv[3]) as data_file:
    ufo_data = json.loads(data_file.read())

for i in ufo_data:
    year = int(i['sighted_at'][:4])
    if year>int(sys.argv[4]) and year<int(sys.argv[5]):
        tmpt = [x.strip() for x in i['location'].split(',')]
        city = tmpt[0]
        for j in city_data:
            if j['city'] == city:
                county = j['county_name']
                break
        for k in drug_data:
            t = k[4].split(" ")
            drug_county = ""
            for p in range(len(t)-1):
                if p == 0:
                    drug_county+=" "+t[p][1:]
                else:
                    drug_county+=" "+t[p]
            if int(k[1]) == year and drug_county.strip()== county:
                i['population'] = k[6]
                i['death rate'] = k[7]
                break






for i in ufo_data:
    tmpt = [x.strip() for x in i['location'].split(',')]
    city = tmpt[0]
    for j in city_data:
        if j['city'] == city:
            county = j['county_name']
            if i['county'] == "":
                i['county'] = county
            break

# with open('disease_ufo_2014_4.json', 'w') as outfile:
with open(sys.argv[6], 'w') as outfile:
    json.dump(ufo_data, outfile)