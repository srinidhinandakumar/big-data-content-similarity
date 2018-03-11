
# Splits a single json into multiple files for parallel processing

#!/usr/bin/python

import json

fileUFO = '../intermediate/ufo_final.json'

data = json.load(open(fileUFO))

count = 1
temp = []

for i in range(len(data)):
    temp.append(data[i])
    if (i+1)%7500 == 0:
        fileName = "ufo"+str(count)+".json"
        with open(fileName, 'w') as outfile:
            json.dump(temp, outfile, indent=4)
        count += 1
        temp = []

fileName = "ufo"+str(count)+".json"
with open(fileName, 'w') as outfile:
    json.dump(temp, outfile, indent=4)
