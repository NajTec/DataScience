import pandas as pd
import matplotlib.pyplot as plt 
from datetime import datetime
import numpy as np

covid_data = pd.read_csv('RKI_COVID19.csv')
feinstaub_data = pd.read_csv('Luftqualitaet.csv',sep=';')


mannheim_data = covid_data[covid_data['Landkreis'] == 'SK Mannheim' ]
sorted_mannheimdata = mannheim_data.sort_values(by='Refdatum')

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



covid_mannheim_2020 = sorted_mannheimdata[sorted_mannheimdata['Refdatum'] <= '2020/12/31 00:00:00' ]
plt.plot(covid_mannheim_2020['Refdatum'],covid_mannheim_2020['AnzahlFall'])

plt.plot(new_date,new['Feinstaub (PM₁₀) stündlich gleitendes Tagesmittel in µg/m³'])