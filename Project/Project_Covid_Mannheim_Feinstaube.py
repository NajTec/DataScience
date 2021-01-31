#Abhängigkeiten importieren

import pandas as pd
import matplotlib.pyplot as plt 
from datetime import datetime
import numpy as np
from scipy.stats import pearsonr
import collections
from scipy.ndimage.filters import uniform_filter1d

#%%

#Daten aus Datei auslesen

covid_data_germany = pd.read_csv('RKI_COVID19.csv')
feinstaub_data_mannheim = pd.read_csv('Luftqualitaet.csv',sep=';')

#%%

#Corona Daten nach Landkreis Mannheim filtern
covid_data_mannheim = covid_data_germany[covid_data_germany['Landkreis'] == 'SK Mannheim' ]
#Corona Daten nach Datum sortieren
#sortedByDate_covid_data_mannheim = covid_data_mannheim.sort_values(by='Refdatum')

#2021 Werte aussortiert
covid_data_mannheim = covid_data_mannheim[
        covid_data_mannheim['Refdatum'] <= '2020/12/31 00:00:00' ]

#%%

#Tage an denen nicht aufgenommen wurde aussortieren
feinstaub_data_mannheim = feinstaub_data_mannheim[feinstaub_data_mannheim['Feinstaub (PM₁₀) stündlich gleitendes Tagesmittel in µg/m³'] != '-']

#Umweltbundesamt Eintrag aussortieren
feinstaub_data_mannheim = feinstaub_data_mannheim[:-2]
#%%

#Fallzahlen und Todeszahlen pro Tag bestimmen

neuinfektionen_nach_datum = {}
todesfaelle_nach_datum = {}

for key, value in enumerate(covid_data_mannheim['Refdatum']):
    if value[:10] not in neuinfektionen_nach_datum:
        todesfaelle_nach_datum[value[:10]] = [np.array(covid_data_mannheim['AnzahlTodesfall'])[key]]
        neuinfektionen_nach_datum[value[:10]] = [np.array(covid_data_mannheim['AnzahlFall'])[key]]
    else:
        todesfaelle_nach_datum[value[:10]].append(np.array(covid_data_mannheim['AnzahlTodesfall'])[key])
        neuinfektionen_nach_datum[value[:10]].append(np.array(covid_data_mannheim['AnzahlFall'])[key])
        
        wert = neuinfektionen_nach_datum[value[:10]]
        neuinfektionen_nach_datum[value[:10]] = [np.sum(np.array(wert))]
    
        wert = todesfaelle_nach_datum[value[:10]]
        todesfaelle_nach_datum[value[:10]] = [np.sum(np.array(wert))]
        
#%%

#Tagesmittel Feinstaub (PM₁₀) pro Tag bestimmen

feinstaub_data_mannheim_nach_datum = {}

for key, value in enumerate(feinstaub_data_mannheim['Datum']):
    if type(value) is float:
        break;
        
    new_date = str(datetime.strptime(value[:10],"%d.%m.%Y"))[:10]
    
    if new_date not in feinstaub_data_mannheim_nach_datum:
        
        feinstaub_data_mannheim_nach_datum[new_date] = [np.array(feinstaub_data_mannheim['Feinstaub (PM₁₀) stündlich gleitendes Tagesmittel in µg/m³'])[key]]
    else:
        
        feinstaub_data_mannheim_nach_datum[new_date].append(np.array(feinstaub_data_mannheim['Feinstaub (PM₁₀) stündlich gleitendes Tagesmittel in µg/m³'])[key])

#Tage an denen nicht aufgenommen wurde mit 0 auffüllen
for datum in feinstaub_data_mannheim_nach_datum.keys():
    
    if datum.replace("-", "/") not in neuinfektionen_nach_datum.keys():
        neuinfektionen_nach_datum[datum.replace("-", "/")] = [0]
        todesfaelle_nach_datum[datum.replace("-", "/")] = [0]
    
    feinstaub_data_mannheim_nach_datum[datum] = np.mean(np.array(feinstaub_data_mannheim_nach_datum[datum]))
    
#%%
    
#Datum in richtiger Reihenfolge
sorted_neuinfektionen_nach_datum = collections.OrderedDict(sorted(neuinfektionen_nach_datum.items()))
sorted_todesfaelle_nach_datum = collections.OrderedDict(sorted(todesfaelle_nach_datum.items()))
sorted_feinstaub_data_mannheim_nach_datum = collections.OrderedDict(sorted(feinstaub_data_mannheim_nach_datum.items()))

anzahl_faelle_list = list(sorted_neuinfektionen_nach_datum.values())
anzahl_tode_list = list(sorted_todesfaelle_nach_datum.values())
feinstaub_list = list(sorted_feinstaub_data_mannheim_nach_datum.values())

for key, value in enumerate(anzahl_faelle_list):
    anzahl_faelle_list[key] = anzahl_faelle_list[key][0]
    anzahl_tode_list[key] = anzahl_tode_list[key][0]

#%%

plt.scatter(feinstaub_list, anzahl_faelle_list)
plt.ylabel("Neuinfektionen nach Datum")
plt.xlabel("Tagesmittel Feinstaub (PM₁₀) nach Datum")
plt.show()

plt.plot(anzahl_faelle_list) 
plt.plot(anzahl_tode_list)
plt.plot(feinstaub_list)
plt.xlabel("25.02.2020 - 31.12.2020")
plt.show()

plt.plot(anzahl_faelle_list[220:])
plt.plot(anzahl_tode_list[220:])
plt.plot(feinstaub_list[220:])
plt.xlabel("??? - 31.12.2020")
plt.show()

fig, axs = plt.subplots(2,2)
fig.suptitle('Vertically stacked subplots')
axs[0,0].scatter(anzahl_faelle_list, anzahl_tode_list)
axs[0,1].scatter(anzahl_faelle_list[:-1], anzahl_tode_list[1:])
axs[1,0].scatter(anzahl_faelle_list[:-2], anzahl_tode_list[2:])
axs[1,1].scatter(anzahl_faelle_list[:-3], anzahl_tode_list[3:])
plt.show()

N = 7
anzahl_faelle_list_rm = uniform_filter1d(anzahl_faelle_list, size=N)
anzahl_tode_list_rm = uniform_filter1d(anzahl_tode_list, size=N)

plt.plot(anzahl_faelle_list_rm[220:])
plt.plot(anzahl_tode_list_rm[220:] * 10)
plt.show()

corrs = []
for i in range(1,50):
    corr,p= pearsonr(anzahl_faelle_list_rm[:-i], anzahl_tode_list_rm[i:])
    corrs.append(corr)
    
plt.plot(corrs)
plt.xlabel("Korrelation im Täglichen shift (Mannheim)")
plt.show()

#%%
"""
covid_data_germany = pd.read_csv('covid-19.csv',sep=';')

faelle_nach_datum = list(covid_data_germany['Faelle'])
todesfaelle_nach_datum = list(covid_data_germany['Todesfaelle'])

plt.plot(faelle_nach_datum) 
plt.plot(todesfaelle_nach_datum)
plt.xlabel("02.01.2020 - 31.12.2020")
plt.show()

plt.plot(faelle_nach_datum[220:])
plt.plot(todesfaelle_nach_datum[220:])
plt.xlabel("??? - 31.12.2020")
plt.show()

N = 7
anzahl_faelle_list_rm = uniform_filter1d(faelle_nach_datum, size=N)
anzahl_tode_list_rm = uniform_filter1d(todesfaelle_nach_datum, size=N)

plt.plot(anzahl_faelle_list_rm)
plt.plot(anzahl_tode_list_rm)
plt.xlabel("02.01.2020 - 31.12.2020 - uniform_filter1d")
plt.show()

plt.plot(anzahl_faelle_list_rm[220:])
plt.plot(anzahl_tode_list_rm[220:] * 10)
plt.xlabel("??? - 31.12.2020 - uniform_filter1d")
plt.show()

anzahl_faelle_list_rm = anzahl_faelle_list_rm[:-16]
anzahl_tode_list_rm = anzahl_tode_list_rm[:-16]
    
corrs = []
for i in range(1,50):
    corr,p= pearsonr(anzahl_faelle_list_rm[220:-i], anzahl_tode_list_rm[220+i:])
    corrs.append(corr)
    
plt.plot(corrs)
plt.show()
"""