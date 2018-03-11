# extracts features from airport and pollution dataset and adds it to ufo dataset

#!/usr/bin/python

import pandas as pd
import os.path
import geopy.distance
import json

class AddFeatures:

    path = os.path.dirname(__file__)
    fileMergeAirportUFO = ""
    fileMergeAirpAirUFO = ""
    fileAirport = ""
    fileUFO = ""
    fileAir = ""

    def __init__(self):
        self.fileUFO = '/../datasets/ufo_final.json'
        self.fileAirport = '/../datasets/airports.csv'
        self.fileAir = '/../datasets/air_poll_lat_long.json'
        self.fileMergeAirportUFO = "ufo_airport.json"
        self.fileMergeAirpAirUFO = "ufo_airport_air.json"

    def accessUFOdata(self):
        file =  self.path + self.fileUFO
        return json.load(open(file))

    def accessAirportData(self):
        file = self.path + self.fileAirport
        return pd.read_csv(file)

    def accessAirpollutionData(self):
        file = self.path + self.fileAir
        return json.load(open(file))

    def accessUFOAirpMergeData(self):
        return json.load(open(self.fileMergeAirportUFO))

    def addAirpollutionFeatures(self, air):
        u = self.accessUFOAirpMergeData()
        look_up = {}
        all_count = 0
        success_count = 0
        error_count = 0
        invalid_indices_lalo = []
        threshold = 100

        for i in range(len(u)):
            minVal = 1000001
            co = ""
            so2 = ""
            o3 = ""
            all_count += 1
            temp = u[i]

            # if the location is already present in the map
            loc = temp['location']
            if loc in look_up:
                print "Already present: ", look_up[loc]
                success_count += 1
                temp['O3 Mean'] = look_up[loc][0]
                temp['SO2 Mean'] = look_up[loc][1]
                temp['CO Mean'] = look_up[loc][2]
                continue

            if "latitude" in temp and "longitude" in temp:
                lat = temp['latitude']
                long = temp['longitude']
            else:
                temp['latitude'] = ""
                temp['longitude'] = ""

            # invalid entries
            if not lat or not long:
                error_count += 1
                invalid_indices_lalo.append(i)
                temp['O3 Mean'] = ""
                temp['SO2 Mean'] = ""
                temp['CO Mean'] = ""
                print loc, "Invalid"
                continue

            coords_1 = (lat, long)

            for j in range(len(air)):
                if "latitude" in air[i] and "longitude" in air[i]:
                    coords_2 = (air[i]['latitude'], air[i]['longitude'])
                else:
                    continue
                if not coords_2[0] or not coords_1[1]:
                    continue
                try:
                    val = geopy.distance.great_circle(coords_1, coords_2).mi
                    if minVal > val:
                        minVal = val
                        o3 = air[i]['O3 Mean']
                        so2 = air[i]['SO2 Mean']
                        co = air[i]['CO Mean']
                except:
                    continue

            if minVal < threshold and (o3 or so2 or co):
                success_count += 1
                temp['O3 Mean'] = o3
                temp['SO2 Mean'] = so2
                temp['CO Mean'] = co
                look_up[loc] = (o3, so2, co)
            else:
                error_count += 1
                invalid_indices_lalo.append(i)
                temp['O3 Mean'] = ""
                temp['SO2 Mean'] = ""
                temp['CO Mean'] = ""

            print loc, minVal, o3, so2, co

        with open(self.fileMergeAirpAirUFO, 'w') as outfile:
            json.dump(u, outfile, indent=4)

        print "Success entries: ", success_count
        print "Error entires: ", error_count
        print "Total entries: ", all_count
        print "Invalid indices: ", invalid_indices_lalo

    def addAirportFeatures(self, airport):
        look_up = {}
        all_count = 0
        success_count = 0
        error_count = 0
        u = self.accessUFOdata()
        invalid_indices_lalo = []
        threshold = 700

        for i in range(len(u)):
            minVal = 1000001
            airport_name = ""
            all_count += 1
            temp = u[i]

            # if the location is already present in the map
            loc = temp['location'].encode('utf8')
            if loc in look_up:
                print "Already present: ", all_count, loc, look_up[loc]
                success_count += 1
                temp['airport_distance'] = look_up[loc][0]
                temp['airport_name'] = look_up[loc][1]
                continue

            if "latitude" in temp and "longitude" in temp:
                lat = temp['latitude']
                long = temp['longitude']
            else:
                temp['latitude'] = ""
                temp['longitude'] = ""

            # invalid entries
            if not lat or not long:
                error_count += 1
                invalid_indices_lalo.append(i)
                temp['airport_distance'] = ""
                temp['airport_name'] = ""
                print all_count, loc, "Invalid"
                continue

            coords_1 = (lat, long)

            for index, row in airport.iterrows():
                coords_2 = (row["latitude_deg"], row["longitude_deg"])
                if not coords_2[0] or not coords_1[1]:
                    continue
                try:
                    val = geopy.distance.great_circle(coords_1, coords_2).mi
                    if minVal > val:
                        minVal = val
                        airport_name = row["name"]
                except:
                    continue

            if minVal < threshold and airport_name:
                success_count += 1
                temp['airport_distance'] = minVal
                temp['airport_name'] = airport_name
                look_up[loc] = (minVal, airport_name)
            else:
                error_count += 1
                invalid_indices_lalo.append(i)
                temp['airport_distance'] = ""
                temp['airport_name'] = ""

            print all_count, loc, minVal, airport_name

        # write to the file
        with open(self.fileMergeAirportUFO, 'w') as outfile:
            json.dump(u, outfile, indent=4)


        print "Success entries: ", success_count
        print "Error entires: ", error_count
        print "Total entries: ", all_count
        print "Invalid indices: ", invalid_indices_lalo

    def addFeaturesForDatasets(self):
        air = self.accessAirpollutionData()
        airport = self.accessAirportData()
        self.addAirportFeatures(airport)
        print "------------------------------"
        print "------------------------------"
        self.addAirpollutionFeatures(air)


if __name__ == "__main__":
    obj = AddFeatures()
    obj.addFeaturesForDatasets()
