import time
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class Latlong:
    def generate_latlong(self, address, geolocator, sentence):
        # print(sentence)
        sentence['latitude'] = ""
        sentence['longitude'] = ""
        try:
            location = geolocator.geocode(address, timeout=5)

            if location != None:
                lat = location.latitude
                long = location.longitude

                sentence['latitude'] = lat
                sentence['longitude'] = long
                # sentence['isset-latlong'] = latlong
        except GeocoderTimedOut as e:
            print("Error: geocode failed on input %s with message %s" % e.msg)

        return sentence

    def parse_latlong(self, filename1, filename2, filename3):

        f1 = open(filename1, 'r')
        data = json.load(f1)
        f2 = open(filename2, 'r')
        location = json.load(f2)
        f3 = open(filename3, 'a')
        # f3.write("[")
        new_data = []

        # data = f.read()
        geolocator = Nominatim(scheme='http')
        count = 0
        for line in data:
            # new_line = dict()
            # print(location['data'])
            if line['location'] in location['data']:
                new_line = line
                new_line['latitude'] = location['data'][line['location']][0]
                new_line['longitude'] = location['data'][line['location']][1]
                new_line = str(new_line).replace('\'', '\"')
                new_data.append(line)

            else:
                count += 1
                if count > 1200:
                    text = input("prompt: ")
                    count = 0
                    print(text+" count: "+str(count))

                # print(str(line['location']))
                print(str(count))
                new_line = self.generate_latlong(line['location'], geolocator, line)
                location['data'][new_line['location']] = [new_line['latitude'], new_line['longitude']]
                new_line = str(new_line).replace('\'', '\"')
                new_data.append(new_line)
            # count += 1
            f3.write(str(new_line)+",")

        f2 = open(filename2, 'w')
        json.dump(location, f2, indent=4)
        print(count)
        # f3.write("]")
        return new_data


t1 = time.time()
if __name__ == "__main__":
    file1 = "../data/intermediate_datasets/ufo_awesome_withlatlong_forCompare.json"
    file2 = "../data/intermediate_datasets/location.json"
    file3 = "../data/intermediate_datasets/ufo_awesome_withlatlong_resultX.json"
    file4 = "../data/intermediate_datasets/ufo_awesome_withlatlong_forCompare.json"
    model = Latlong()
    final_data = model.parse_latlong(file1, file2, file3)
    # f = open(file4, 'w')
    # json.dump(f, final_data, indent=4)
t2 = time.time()
print("Time: "+str(t2-t1))
