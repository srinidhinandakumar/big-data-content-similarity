# Ideal threshold value for reduced_100.json dataset 0.0001 to 0.0004

try:
    import simplejson as json
except ImportError:
    import json

import sys

default_threshold = 0.0003

usage = "Usage: python cluster-scores.py [-t threshold_value]"

def main(threshold):
    with open("similarity-scores.txt") as f:
        prior = None
        clusters = []
        clusterCount = 0
        cluster = {"name":"cluster"+str(clusterCount)}
        clusterData = []
        for line in f:
            if line.find("{") != -1:
                featureDataList = line.split(",",3) # file name,score,metadata
            else :
                featureDataList = line.split(",", 2)

            if not (len(featureDataList) == 3 or len(featureDataList) == 4):
                continue


            if prior != None:
                diff = prior-float(featureDataList[1])
            else:
                diff = -1.0

            # cleanse the \n
            featureDataList[1] = featureDataList[1].strip()
            if(len(featureDataList) == 4):
                featureData = {"name":featureDataList[0], "score":float(featureDataList[1]), "path" :featureDataList[2],  "metadata" : featureDataList[3]}
            elif (len(featureDataList) == 3):
                featureData = {"name":featureDataList[0], "score":float(featureDataList[1]), "path" :featureDataList[2]}

            if diff > threshold:
                cluster["children"] = clusterData
                clusters.append(cluster)
                clusterCount = clusterCount + 1
                cluster = {"name":"cluster"+str(clusterCount)}
                clusterData = []
                clusterData.append(featureData)
                prior = float(featureDataList[1])
            else:
                clusterData.append(featureData)
                prior = float(featureDataList[1])

        #add the last cluster into clusters
        cluster["children"] = clusterData
        clusters.append(cluster)
        clusterCount = clusterCount + 1
        cluster = {"name":"cluster"+str(clusterCount)}

    clusterStruct = {"name":"clusters", "children":clusters}
    with open("clusters.json", "w") as f:
        f.write(json.dumps(clusterStruct, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    threshold = default_threshold
    if len(sys.argv) == 3 and sys.argv[1] == "-t":
        try:
            threshold = float(sys.argv[2])
        except:
            print usage
            print "Using default threshold value..."

    main(threshold)
