import json
import csv
import pandas as pd
import time


# this class uses pandas to filter the final dataset as and when required based on different features
class Datafilter:

    def add_year(self, df):
        df["year"] = df["sighted_at"][0:3]
        return df

    def pd_to_json(self, filename, df):
        out = df.to_json(orient='records')[1:-1].replace('},{', '} {')
        with open(filename, 'w') as f:
            f.write(out)

    def filter_population_county(self, filename):
        f1 = open(filename, 'r')
        data = json.load(f1)
        train = pd.DataFrame.from_dict(data)
        # print(train.head(10))
        # train.reset_index(level=0, inplace=True)
        location_population = train.loc[train["population"] != "", ["county", "population", "death rate"]]
        location_population.drop_duplicates()
        self.pd_to_json('../d3/data-d3/location_population.json', location_population)
        # print(population.head(10))
        # get yearly sightings
        year_only = train.sighted_at.apply(lambda s: pd.Series({'year': pd.to_numeric(s[0:4])}))
        # print(year_only.head())
        year = pd.concat([train, year_only], axis=1)
        # pd.concat([train, train.sighted_at.apply(lambda s: pd.Series({'year':s[0:3]}))], axis=1)
        # year = train["county","location","sighted_at","year"]
        # year.drop_duplicates()
        location_year_1 = year.loc[year["latitude"] != "", ["location", "county", "latitude", "longitude", "sighted_at", "year"]]
        location_year_2 = location_year_1.loc[location_year_1["year"] > 1995]
        location_year_2 = location_year_1.loc[location_year_1["year"] < 2015]
        print(location_year_2.head())
        # self.pd_to_json('../d3/data-d3/location_year.json', location_year_2)


if __name__ == "__main__":
    t1 = time.time()
    filename = "../datasets/intermediate_datasets/dataset_ddu.json"
    model = Datafilter()
    model.filter_population_county(filename)
    t2 = time.time()
    print("Time: " + str(t2 - t1))
