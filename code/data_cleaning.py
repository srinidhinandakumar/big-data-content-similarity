import json
import time
import numpy as np


class Clean:
    def cleaning_errors_latlong(self, file1, file2):
        f1 = open(file1, 'r')
        f2 = open(file2, 'r')
        data1 = json.load(f1)
        data2 = json.load(f2)
        new_data = []
        len1 = len(data1)
        len2 = len(data2)
        print(len1)
        print(len2)
        d1 = list({v['description']: v for v in data1}.values())
        return d1

    def fix_lines(self, json_array, output_file):
        with open(output_file, "w") as text_file:
            json_array = str(json_array).replace('\'', '\"')
            # text_file.write(str(json_array))
            text_file.write(json.dumps(json.loads(json_array), indent=4))

    def remove_error(self, data):
        # data = json.load(open(filename, 'r'))
        for d in data:
            if d["latitude"] == "ERROR":
                d["latitude"] = ""
                d["longitude"] = ""
        return data


if __name__ == "__main__":
    # filename1 = "ufo_awesome_with_lat_long.json"
    filename1 = "../data/intermediate_datasets/1_1.json"
    filename2 = "../data/original_datasets/fixed_ufo_awesome.json"
    model = Clean()
    data = model.cleaning_errors_latlong(filename1, filename2)
    f3 ="../data/intermediate_datasets/fixed2.json"
    f4 ="../data/intermediate_datasets/fixed3.json"

    d = model.remove_error(data)
    model.fix_lines(data, f4)
    # text_file = open(f4, 'w')
    # text_file.write(json.dumps(json.loads(str(d)), indent=4))
    # f = open(f3, 'w')
    # f.write(str(data))
    # json.dumps(f, data, indent=4)
