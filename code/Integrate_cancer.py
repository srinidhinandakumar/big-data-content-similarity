import json
import sys

state = ['Alabama', 'Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois',\
         'Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota'	,'Mississippi','Missouri',\
         'Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York',	'North Carolina','North Dakota','Ohio','Oklahoma','Oregon',\
         'Pennsylvania','Rhode Island'	,'South carolina','South dakota','Tennessee'	,'Texas'	,'Utah','Vermont','Virginia','Washington','West Virginia',\
         'Wisconsin','Wyoming']

state_abbr = ['AL','AK'	,'AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN',\
              'MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT',\
              'VA','WA','WV','WI','WY']

# inputfile = open("/Users/weiweiduan/Downloads/CS599_assign1/Table_2014.txt", "r")
inputfile = open(sys.argv[1], "r")
disease_dict = {}
for line in inputfile:
    tmpt = line.strip().split("\t")
    if len(tmpt) == 5:
        disease_dict[tmpt[0]] = {'all races':tmpt[1], 'white':tmpt[2], 'black':tmpt[3], 'hispanic':tmpt[4]}


with open('disease_ufo_2013.json') as data_file:
    data = json.loads(data_file.read())
for i in data:
    if sys.argv[2] in i['sighted_at']:
        tmpt = [x.strip() for x in i['location'].split(',')]
        abbr = tmpt[1]
        if abbr in state_abbr:
            indice = state_abbr.index(abbr)
            if state[indice] in disease_dict:
                i['cancer_incidence_counts_allraces'] = disease_dict[state[indice]]['all races']
                i['cancer_incidence_counts_white'] = disease_dict[state[indice]]['white']
                i['cancer_incidence_counts_black'] = disease_dict[state[indice]]['black']
                i['cancer_incidence_counts_hispanic'] = disease_dict[state[indice]]['hispanic']

        else:
            i['cancer_incidence_counts_allraces'] = ""
            i['cancer_incidence_counts_white'] = ""
            i['cancer_incidence_counts_black'] = ""
            i['cancer_incidence_counts_hispanic'] = ""
#
# with open('disease_ufo_2014.json', 'w') as outfile:
with open(sys.argv[3], 'w') as outfile:
    json.dump(data, outfile)

