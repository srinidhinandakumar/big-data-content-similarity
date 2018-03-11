# Performs Jaccard distance algorithm for features in a particular file
# Usage : python features_jaccard.py -f fileName

import tika
from tika import parser
import sys
import operator
from time import sleep
from requests import ConnectionError
import ast

def main(argv = None):
    if argv is None:
        argv = sys.argv
    if len(argv) != 3:
        sys.exit(0)

    union_feature_names = set()
    row_parsed_data = {}
    resemblance_scores = {}
    filename = argv[2]

    try:
        parsedData = parser.from_file(filename)
    except ConnectionError:
        sleep(1)
    except KeyError:
        exit(0)

    parsedData = ast.literal_eval(parsedData['content'])

    # count similarity for two given files
    for i in range(len(parsedData)):
        # first compute the union of all features
        row_parsed_data[i] = parsedData[i]
        union_feature_names = union_feature_names | set(row_parsed_data[i].values())

    total_num_features = len(union_feature_names)

    #compute the specific resemblance and containment scores
    for row in row_parsed_data:
        overlap = {}
        overlap = set(row_parsed_data[row].values()) & set(union_feature_names)
        resemblance_scores[row] = round((float(len(overlap)) / total_num_features), 4)

    sorted_resemblance_scores = sorted(resemblance_scores.items(), key=operator.itemgetter(1), reverse=True)

    with open("similarity-scores.txt", "w") as f:
        f.write("Resemblance : \n")
        for tuple in sorted_resemblance_scores:
            f.write(
                str(tuple[0]) + "," + str(tuple[1]) + "," + str(tuple[0]) + "," +
                    convertUnicode(row_parsed_data[tuple[0]]) + '\n')


def convertUnicode(fileDict):
    fileUTFDict = {}
    for key in fileDict:
        if isinstance(key, unicode):
            key = key.encode('utf-8').strip()
        value = fileDict.get(key)
        if isinstance(value, unicode):
            value = value.encode('utf-8').strip()
        fileUTFDict[key] = value

    return str(fileUTFDict)


if __name__ == "__main__":
    sys.exit(main())






