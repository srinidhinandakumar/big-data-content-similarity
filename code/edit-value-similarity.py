#!/usr/bin/env python2.7
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

from tika import parser
import os, editdistance, itertools, argparse, csv
from requests import ConnectionError
from time import sleep
import json
import ast


def stringify(attribute_value):
    if isinstance(attribute_value, list):
        return str((", ".join(attribute_value)).encode('utf-8').strip())
    else:
        return str(str(attribute_value).encode('utf-8').strip())


def computeScores(inputDir, outCSV, acceptTypes, allKeys):

    na_metadata = ["resourceName"]
    with open(outCSV, "wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])

        filename_list = []

        for root, dirnames, files in os.walk(inputDir):
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            for filename in files:
                if not filename.startswith('.'):
                    filename_list.append(os.path.join(root, filename))
        try:
            filename_list = [filename for filename in filename_list if "metadata" in parser.from_file(filename)]
        except ConnectionError:
            sleep(1)

        

        if acceptTypes:
            filename_list = [filename for filename in filename_list if str(parser.from_file(filename)['metadata']['Content-Type'].encode('utf-8')).split('/')[-1] in acceptTypes]
        else:
            print "Accepting all MIME Types....."

        files_tuple = itertools.combinations(filename_list, 2)
        for file1, file2 in files_tuple:
            try:           
                row_edit_distance = [file1, file2]            

                file1_parsedData = parser.from_file(file1)
                file2_parsedData = parser.from_file(file2)
                
                intersect_features = set(file1_parsedData["metadata"].keys()) & set(file2_parsedData["metadata"].keys()) 
                            
                intersect_features = [feature for feature in intersect_features if feature not in na_metadata ]

                file_edit_distance = 0.0
                for feature in intersect_features:

                    file1_feature_value = stringify(file1_parsedData["metadata"][feature])
                    file2_feature_value = stringify(file2_parsedData["metadata"][feature])

                    if len(file1_feature_value) == 0 and len(file2_feature_value) == 0:
                        feature_distance = 0.0
                    else:
                        feature_distance = float(editdistance.eval(file1_feature_value, file2_feature_value))/(len(file1_feature_value) if len(file1_feature_value) > len(file2_feature_value) else len(file2_feature_value))
                    
                    file_edit_distance += feature_distance

            
                if allKeys:
                    file1_only_features = set(file1_parsedData["metadata"].keys()) - set(intersect_features)
                    file1_only_features = [feature for feature in file1_only_features if feature not in na_metadata]

                    file2_only_features = set(file2_parsedData["metadata"].keys()) - set(intersect_features)
                    file2_only_features = [feature for feature in file2_only_features if feature not in na_metadata]

                    file_edit_distance += len(file1_only_features) + len(file2_only_features)       # increment by 1 for each disjunct feature in (A-B) & (B-A), file1_disjunct_feature_value/file1_disjunct_feature_value = 1
                    file_edit_distance /= float(len(intersect_features) + len(file1_only_features) + len(file2_only_features))

                else:
                    file_edit_distance /= float(len(intersect_features))    #average edit distance

                row_edit_distance.append(1-file_edit_distance)
                a.writerow(row_edit_distance)

            except ConnectionError:
                sleep(1)
            except KeyError:
                continue


def compute_score2(json_input_list, outCSV, acceptTypes, allKeys):
    na_metadata = ["resourceName"]
    with open(outCSV, "wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])

        json_list = []
        for each in json_input_list:
            with open(each) as json_input_file:
                json_list.extend(json.load(json_input_file))
        # each object in json_list contains a key as file name and a value: as metadata JSON object

        metadata_dict = {}
        for entry in json_list:
            key = entry.keys()[0]
            metadata_dict[key] = entry[key]

        files_tuple = itertools.combinations(metadata_dict.keys(), 2)
        for file1, file2 in files_tuple:
            try:
                row_edit_distance = [file1, file2]

                file1_metadata = metadata_dict[file1]
                file2_metadata = metadata_dict[file2]

                intersect_features = set(file1_metadata.keys()) & set(file2_metadata.keys())

                intersect_features = [feature for feature in intersect_features if feature not in na_metadata ]

                file_edit_distance = 0.0
                for feature in intersect_features:

                    file1_feature_value = stringify(file1_metadata[feature])
                    file2_feature_value = stringify(file2_metadata[feature])

                    if len(file1_feature_value) == 0 and len(file2_feature_value) == 0:
                        feature_distance = 0.0
                    else:
                        feature_distance = float(editdistance.eval(file1_feature_value, file2_feature_value))/(len(file1_feature_value) if len(file1_feature_value) > len(file2_feature_value) else len(file2_feature_value))

                    file_edit_distance += feature_distance

                if allKeys:
                    file1_only_features = set(file1_metadata.keys()) - set(intersect_features)
                    file1_only_features = [feature for feature in file1_only_features if feature not in na_metadata]

                    file2_only_features = set(file2_metadata.keys()) - set(intersect_features)
                    file2_only_features = [feature for feature in file2_only_features if feature not in na_metadata]

                    file_edit_distance += len(file1_only_features) + len(file2_only_features)       # increment by 1 for each disjunct feature in (A-B) & (B-A), file1_disjunct_feature_value/file1_disjunct_feature_value = 1
                    file_edit_distance /= float(len(intersect_features) + len(file1_only_features) + len(file2_only_features))

                else:
                    file_edit_distance /= float(len(intersect_features))    #average edit distance

                row_edit_distance.append(1-file_edit_distance)
                a.writerow(row_edit_distance)

            except ConnectionError:
                sleep(1)
            except KeyError:
                continue
    return


def computeScores3(inputFile, outCSV):
    na_metadata = ["resourceName"]
    with open(outCSV, "wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate", "y-coordinate", "Similarity_score"])

        file1_parsedData = parser.from_file(inputFile)
        row_list = ast.literal_eval(file1_parsedData["content"])

        rows_tuple = itertools.combinations(row_list, 2)
        counter = 0
        for row1, row2 in rows_tuple:
            print(counter)
            counter += 1
            try:
                row_edit_distance = [row_list.index(row1), row_list.index(row2)]

                content_1 = row1 #ast.literal_eval(file1_parsedData["content"])[0]
                content_2 = row2 #ast.literal_eval(file2_parsedData["content"])[0]

                intersect_features = set(content_1.keys()) & set(content_2.keys())

                intersect_features = [feature for feature in intersect_features if feature not in na_metadata]

                file_edit_distance = 0.0
                for feature in intersect_features:

                    file1_feature_value = stringify(content_1[feature])
                    file2_feature_value = stringify(content_2[feature])

                    if len(file1_feature_value) == 0 and len(file2_feature_value) == 0:
                        feature_distance = 0.0
                    else:
                        feature_distance = float(editdistance.eval(file1_feature_value, file2_feature_value)) / (
                        len(file1_feature_value) if len(file1_feature_value) > len(file2_feature_value) else len(
                            file2_feature_value))

                    file_edit_distance += feature_distance

                file_edit_distance /= float(len(intersect_features))  # average edit distance

                row_edit_distance.append(1 - file_edit_distance)
                a.writerow(row_edit_distance)

            except ConnectionError:
                sleep(1)
            except KeyError:
                continue


if __name__ == "__main__":
    
    argParser = argparse.ArgumentParser('Edit Distance Similarity based on Metadata values')
    argParser.add_argument('--inputDir', required=False, help='path to directory containing files')
    argParser.add_argument('--inputFile', required=False, help='path to input file')
    argParser.add_argument('--outCSV', required=True, help='path to directory for storing the output CSV File, containing pair-wise Similarity Scores based on edit distance')
    argParser.add_argument('--json', nargs='+', required=False, help='several paths to  JSON file containing certain metadata')
    argParser.add_argument('--accept', nargs='+', type=str, help='Optional: compute similarity only on specified IANA MIME Type(s)')
    argParser.add_argument('--allKeys', action='store_true', help='compute edit distance across all keys')
    args = argParser.parse_args()

    if args.inputFile and args.outCSV:
        computeScores3(args.inputFile, args.outCSV)
    if args.inputDir and args.outCSV:
        computeScores(args.inputDir, args.outCSV, args.accept, args.allKeys)
    if args.json:
        compute_score2(args.json, args.outCSV, args.accept, args.allKeys)
