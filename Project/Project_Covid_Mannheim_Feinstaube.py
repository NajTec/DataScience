import pandas as pd
import matplotlib.pyplot as plt 
from datetime import datetime
import numpy as np
from scipy.stats import pearsonr
import operator

covid_data = pd.read_csv('RKI_COVID19.csv')
feinstaub_data = pd.read_csv('Luftqualitaet.csv',sep=';')


mannheim_data = covid_data[covid_data['Landkreis'] == 'SK Mannheim' ]
sorted_mannheimdata = mannheim_data.sort_values(by='Refdatum')
sorted_mannheimdata = sorted_mannheimdata[sorted_mannheimdata['Refdatum'] <= '2020/12/31 00:00:00' ]

sorted_feinstaubdata = feinstaub_data[feinstaub_data['Feinstaub (PM₁₀) stündlich gleitendes Tagesmittel in µg/m³'] != '-']
new = sorted_feinstaubdata[:-2]

#print(feinstaub_data.head())
print(type(sorted_feinstaubdata['Datum'][0]))
print(type(covid_data['Refdatum'][0]))

#print(new)
#date_ = [x.replace("'","") for x in new ]
#print(date_)
new_date = [datetime.strptime(x,"%d.%m.%Y %H:%M") for x in new['Datum'] ]
print(new_date)

dict_with_values = {}

for key, value in enumerate(sorted_mannheimdata['Refdatum']):
    #print(value[:10])
    if value[:10] not in dict_with_values:
        
        dict_with_values[value[:10]] = [np.array(sorted_mannheimdata['AnzahlFall'])[key]]
    else:
        
        dict_with_values[value[:10]].append(np.array(sorted_mannheimdata['AnzahlFall'])[key])

corona_faelle = {}
keys_of_dict = list(dict_with_values.keys())

for key, value in enumerate(dict_with_values):
    value = np.array(dict_with_values[keys_of_dict[key]])
    corona_faelle[keys_of_dict[key]] = np.sum(value)

pd_corona_faelle = pd.DataFrame.from_dict(corona_faelle, orient='index', columns=['Anzahl'])
pd_corona_faelle = pd_corona_faelle[pd_corona_faelle.index <= '2020/12/31' ]

sorted_feinstaubdata = feinstaub_data[feinstaub_data['Feinstaub (PM₁₀) stündlich gleitendes Tagesmittel in µg/m³'] != '-']
new = sorted_feinstaubdata[:-2]

fs_dict_with_values = {}

for key, value in enumerate(sorted_feinstaubdata['Datum']):
    if type(value) is float:
        break;
        
    new_date = str(datetime.strptime(value[:10],"%d.%m.%Y"))[:10]
    
    if new_date not in fs_dict_with_values:
        
        fs_dict_with_values[new_date] = [np.array(sorted_feinstaubdata['Feinstaub (PM₁₀) stündlich gleitendes Tagesmittel in µg/m³'])[key]]
    else:
        
        fs_dict_with_values[new_date].append(np.array(sorted_feinstaubdata['Feinstaub (PM₁₀) stündlich gleitendes Tagesmittel in µg/m³'])[key])

fs_dict_with_values.pop('2021-01-01')

for datum in fs_dict_with_values.keys():
    
    if datum.replace("-", "/") not in corona_faelle.keys():
        corona_faelle[datum.replace("-", "/")] = 0
    
    fs_dict_with_values[datum] = np.mean(np.array(fs_dict_with_values[datum]))
        
sorted_dict = sorted(corona_faelle.items(), key=operator.itemgetter(1))

plt.scatter(fs_dict_with_values.values(), corona_faelle.values())

corr,_= pearsonr(fs_dict_with_values.values(), corona_faelle.values())