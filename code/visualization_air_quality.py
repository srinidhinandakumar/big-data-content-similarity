import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
from matplotlib.colors import LinearSegmentedColormap
import json
import sys

coor_state = {'Alabama':[32.806671,-86.791130], 'Alaska':[61.370716,152.404419],'Arizona':[33.729759,-111.431221],'Arkansas':[34.969704,	-92.373123],\
'California':[36.116203,-119.681564],'Colorado':[39.059811,	-105.311104],'Connecticut':	[41.597782,	-72.755371],\
'Delaware':	[39.318523,	-75.507141],'District of Columbia':	[38.897438,	-77.026817],'Florida':	[27.766279,	-81.686783],\
'Georgia':	[33.040619,	-83.643074],'Hawaii':	[21.094318,	-157.498337],'Idaho':[44.240459,-114.478828],'Illinois':[40.349457,	-88.986137],\
'Indiana':	[39.849426,	-86.258278],'Iowa':	[42.011539,	-93.210526],'Kansas':[38.526600,-96.726486],'Kentucky':	[37.668140,	-84.670067],\
'Louisiana':[31.169546,	-91.867805],'Maine':[44.693947,	-69.381927],'Maryland':	[39.063946,	-76.802101],'Massachusetts':[42.230171,	-71.530106],\
'Michigan':	[43.326618,	-84.536095],'Minnesota':[45.694454,	-93.900192],'Mississippi':[32.741646,-89.678696],'Missouri':[38.456085,	-92.288368],\
'Montana':	[46.921925,	-110.454353],'Nebraska':[41.125370,	-98.268082],'Nevada':[38.313515,-117.055374],'New Hampshire':[43.452492,-71.563896],\
'New Jersey':[40.298904,-74.521011],'New Mexico':[34.840515,-106.248482],'New York':[42.165726,	-74.948051],'North Carolina':[35.630066,-79.806419],\
'North Dakota':	[47.528912,	-99.784012],'Ohio':	[40.388783,	-82.764915],'Oklahoma':	[35.565342,	-96.928917],'Oregon':[44.572021,-122.070938],\
'Pennsylvania':	[40.590752,	-77.209755],'Rhode Island':	[41.680893,	-71.511780],'South Carolina':	[33.856892,	-80.945007],'South Dakota':	[44.299782,	-99.438828],\
'Tennessee':[35.747845,	-86.692345],'Texas':[31.054487,	-97.563461],'Utah':	[40.150032,	-111.862434],'Vermont':	[44.045876,	-72.710686],'Virginia':	[37.769337,	-78.169968],\
'Washington':[47.400902,-121.490494],'West Virginia':[38.491226,-80.954453],'Wisconsin':[44.268543,	-89.616508],'Wyoming':	[42.755966,	-107.302490]}

state = ['Alabama', 'Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois',\
         'Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota'	,'Mississippi','Missouri',\
         'Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York',	'North Carolina','North Dakota','Ohio','Oklahoma','Oregon',\
         'Pennsylvania','Rhode Island'	,'South carolina','South dakota','Tennessee'	,'Texas'	,'Utah','Vermont','Virginia','Washington','West Virginia',\
         'Wisconsin','Wyoming']

state_abbr = ['AL','AK'	,'AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN',\
              'MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT',\
              'VA','WA','WV','WI','WY']

with open(sys.argv[1]) as data_file:
    data = json.loads(data_file.read())

ufo_state = {}
cancer_state = {}
for i in state_abbr:
    ufo_state[i] = 0
    cancer_state[i] = []
lons = []
lats = []
check = []
pollution = {}
for i in data:
    if int(sys.argv[2]) in i['sighted_at']:
     # if '1999' in i['sighted_at'] or '2000' in i['sighted_at'] or '2001' in i['sighted_at'] or '2002' in i['sighted_at'] or '2003' in i['sighted_at'] or '2004' in i['sighted_at'] or '2005' in i['sighted_at'] or '2006' in i['sighted_at'] or '2007' in i['sighted_at'] or '2008' in i['sighted_at']:
    #if '2009' in i['sighted_at'] or '2010' in i['sighted_at'] or '2011' in i['sighted_at'] or '2012' in i['sighted_at'] or '2013' in i['sighted_at']:
        tmpt = [x.strip() for x in i['location'].split(',')]
        abbr = tmpt[1]
        if abbr in state_abbr:
            indice = state_abbr.index(abbr)
            state_name = state[indice]
            if state_name in coor_state and i['O3 Mean'] != "":
                if state_name not in pollution:
                    pollution[state_name] = [int(round(float(i['O3 Mean'])))]
                else:
                    pollution[state_name].append(int(round(float(i['O3 Mean']))))

for i in pollution:
    lons.extend([coor_state[i][1]]*int(sum(pollution[i])/len(pollution[i])))
    lats.extend([coor_state[i][0]]*int(sum(pollution[i])/len(pollution[i])))

#
m = Basemap(projection = 'merc', llcrnrlat=10, urcrnrlat=50,
        llcrnrlon=-160, urcrnrlon=-60)

m.drawcoastlines()
m.drawcountries()
m.drawstates()

db = 1 # bin padding
lon_bins = np.linspace(min(lons)-db, max(lons)+db, 36) # 10 bins
lat_bins = np.linspace(min(lats)-db, max(lats)+db, 18) # 13 bins


density, _, _ = np.histogram2d(lats, lons, [lat_bins, lon_bins])
# Turn the lon/lat of the bins into 2 dimensional arrays ready
# for conversion into projected coordinates
lon_bins_2d, lat_bins_2d = np.meshgrid(lon_bins, lat_bins)


# convert the bin mesh to map coordinates:
xs, ys = m(lon_bins_2d, lat_bins_2d) # will be plotted using pcolormesh
cdict = {'red':  ( (0.0,  1.0,  1.0),
                   (1.0,  0.9,  1.0) ),
         'green':( (0.0,  1.0,  1.0),
                   (1.0,  0.03, 0.0) ),
         'blue': ( (0.0,  1.0,  1.0),
                   (1.0,  0.16, 0.0) ) }
custom_map = LinearSegmentedColormap('custom_map', cdict)
plt.register_cmap(cmap=custom_map)

density = np.hstack((density,np.zeros((density.shape[0],1))))
density = np.vstack((density,np.zeros((density.shape[1]))))

plt.pcolormesh(xs, ys, density, cmap="custom_map", shading='gouraud')

cbar = plt.colorbar(orientation='horizontal', shrink=0.625, aspect=20, fraction=0.2,pad=0.02)
cbar.set_label('SO2 mean',size=18)
#plt.clim([0,100])


# translucent blue scatter plot of epicenters above histogram:
x,y = m(lons, lats)
m.plot(x, y, 'o', markersize=5,zorder=6, markerfacecolor='#424FA4',markeredgecolor="none", alpha=0.33)



# make image bigger:
plt.title('Air quality (SO2 mean) from 2009 to 2013')
plt.gcf().set_size_inches(15,15)

plt.show()
