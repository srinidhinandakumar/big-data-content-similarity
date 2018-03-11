# merger for ufo, airport and pollution dataset

#!/usr/bin/python

import json

pollution = json.load(open("../intermediate/ufo_airport_poll.json"))

airport = json.load(open("../intermediate/dataset_ddu.json"))

print pollution[0]

print len(airport), len(pollution)

count = 0

for i,j in zip(range(len(airport)),range(len(pollution))):
    if airport[i]['location'] == pollution[j]['location']:
        if "cancer_incidence_counts_white" in airport[i]:
            pollution[j]['cancer_incidence_counts_white'] = airport[i]['cancer_incidence_counts_white']
        else:
            pollution[j]['cancer_incidence_counts_white'] = ""

        if "cancer_incidence_counts_hispanic" in airport[i]:
            pollution[j]['cancer_incidence_counts_hispanic'] = airport[i]['cancer_incidence_counts_hispanic']
        else:
            pollution[j]['cancer_incidence_counts_hispanic'] = ""

        if "cancer_incidence_counts_black" in airport[i]:
            pollution[j]['cancer_incidence_counts_hispanic'] = airport[i]['cancer_incidence_counts_hispanic']
        else:
            pollution[j]['cancer_incidence_counts_hispanic'] = ""

        if "cancer_incidence_counts_allraces" in airport[i]:
            pollution[j]['cancer_incidence_counts_allraces'] = airport[i]['cancer_incidence_counts_allraces']
        else:
            pollution[j]['cancer_incidence_counts_allraces'] = ""

        if "population" in airport[i]:
            pollution[j]['population'] = airport[i]['population']
        else:
            pollution[j]['population'] = ""

        if "county" in airport[i]:
            pollution[j]['county'] = airport[i]['county']
        else:
            pollution[j]['county'] = ""

        if "death rate" in airport[i]:
            pollution[j]['death rate'] = airport[i]['death rate']
        else:
            pollution[j]['death rate'] = ""

        count += 1

with open('final.json', 'w') as outfile:
    json.dump(pollution, outfile, indent=4)

print count
