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



inputfile = open(sys.argv[1], "r")
cancer_dict = {}
lons_cancer = []
lats_cancer = []
for line in inputfile:
    tmpt = line.strip().split("\t")
    if len(tmpt) == 5 and tmpt[0] in state and tmpt[0] in coor_state.keys():
        lons_cancer.extend([coor_state[tmpt[0]][1]]*int(tmpt[1].replace(',' , '')))
        lats_cancer.extend([coor_state[tmpt[0]][0]]*int(tmpt[1].replace(',' , '')))

# inputfile = open("Table_2010.txt", "r")
# for line in inputfile:
#     tmpt = line.strip().split("\t")
#     if len(tmpt) == 5 and tmpt[0] in state and tmpt[0] in coor_state.keys():
#         lons_cancer.extend([coor_state[tmpt[0]][1]]*int(tmpt[1].replace(',' , '')))
#         lats_cancer.extend([coor_state[tmpt[0]][0]]*int(tmpt[1].replace(',' , '')))
# inputfile = open("Table_2011.txt", "r")
# for line in inputfile:
#     tmpt = line.strip().split("\t")
#     if len(tmpt) == 5 and tmpt[0] in state and tmpt[0] in coor_state.keys():
#         lons_cancer.extend([coor_state[tmpt[0]][1]]*int(tmpt[1].replace(',' , '')))
#         lats_cancer.extend([coor_state[tmpt[0]][0]]*int(tmpt[1].replace(',' , '')))
# inputfile = open("Table_2012.txt", "r")
# for line in inputfile:
#     tmpt = line.strip().split("\t")
#     if len(tmpt) == 5 and tmpt[0] in state and tmpt[0] in coor_state.keys():
#         lons_cancer.extend([coor_state[tmpt[0]][1]]*int(tmpt[1].replace(',' , '')))
#         lats_cancer.extend([coor_state[tmpt[0]][0]]*int(tmpt[1].replace(',' , '')))
# inputfile = open("Table_2013.txt", "r")
# for line in inputfile:
#     tmpt = line.strip().split("\t")
#     if len(tmpt) == 5 and tmpt[0] in state and tmpt[0] in coor_state.keys():
#         lons_cancer.extend([coor_state[tmpt[0]][1]]*int(tmpt[1].replace(',' , '')))
#         lats_cancer.extend([coor_state[tmpt[0]][0]]*int(tmpt[1].replace(',' , '')))




#
m = Basemap(projection = 'merc', llcrnrlat=10, urcrnrlat=50,
        llcrnrlon=-160, urcrnrlon=-60)

m.drawcoastlines()
m.drawcountries()
m.drawstates()

db = 1 # bin padding
lons_cancer_bin =  np.linspace(min(lons_cancer)-db, max(lons_cancer)+db, 36)
lats_cancer_bin =  np.linspace(min(lats_cancer)-db, max(lats_cancer)+db, 18)

density_cancer, _, _ = np.histogram2d(lats_cancer, lons_cancer, [lats_cancer_bin, lons_cancer_bin])
# Turn the lon/lat of the bins into 2 dimensional arrays ready
# for conversion into projected coordinates
lon_bins_cancer_2d, lat_bin_cancer_2d = np.meshgrid(lons_cancer_bin, lats_cancer_bin)

# convert the bin mesh to map coordinates:
 # will be plotted using pcolormesh
xs_cancer, ys_cancer = m(lon_bins_cancer_2d, lat_bin_cancer_2d)
cdict = {'red':  ( (0.0,  1.0,  1.0),
                   (1.0,  0.9,  1.0) ),
         'green':( (0.0,  1.0,  1.0),
                   (1.0,  0.03, 0.0) ),
         'blue': ( (0.0,  1.0,  1.0),
                   (1.0,  0.16, 0.0) ) }
custom_map = LinearSegmentedColormap('custom_map', cdict)
plt.register_cmap(cmap=custom_map)


density_cancer = np.hstack((density_cancer,np.zeros((density_cancer.shape[0],1))))
density_cancer = np.vstack((density_cancer,np.zeros((density_cancer.shape[1]))))
# add histogram squares and a corresponding colorbar to the map:
plt.pcolormesh(xs_cancer, ys_cancer, density_cancer,cmap="custom_map", shading='gouraud' )

cbar = plt.colorbar(orientation='horizontal', shrink=0.625, aspect=20, fraction=0.2,pad=0.02)
cbar.set_label('Cancer Incidences',size=18)


# make image bigger:
plt.title('Cancer Incidence from 2009 to 2013')
plt.gcf().set_size_inches(15,15)

plt.show()
