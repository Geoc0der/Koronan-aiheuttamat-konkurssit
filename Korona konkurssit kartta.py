# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 19:03:50 2020

@author: larij

Tämän kartan tekemisessä käytettiin ohjeena seuraavaa tutoriaalia:
https://towardsdatascience.com/lets-make-a-map-using-geopandas-pandas-and-matplotlib-to-make-a-chloropleth-map-dddc31c1983d
"""

# Tässä skriptissä haetaan konkurssiin menneiden yritysten lukumäärä kunnittain automaattisesti prh:n
# rajapinnan kautta

import requests
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
from datetime import timedelta
import geopandas as gpd
import pandas as pd
import csv

# Api-osoite konkurssidatalle

url = 'https://avoindata.prh.fi/tr/v1/publicnotices?totalResults=true&maxResults=1000&resultsFrom=0&entryCode=KONALK&noticeRegistrationFrom=2020-01-01'

# asetetaan konkurssidata muuttujaan ja printataan konkurssien määrä ruudulle

konk_data = requests.get(url).json()

print('Total results: ', konk_data['totalResults'])

konk_sum = konk_data['totalResults']

end_date = date.today()

# Eilinen päivä

eilinen = end_date - timedelta(days=1)

# Tuodaan data Suomen yrityskannasta

yrityskanta = pd.read_excel (r'C:\Users\larij\.spyder-py3\Korona konkurssit\Suomen yrityskanta q2 3029.xlsx')

yrityskanta.rename(columns = {'Kunta':'nimi'}, inplace = True)

# Tuodaan shapefile

kunnat = gpd.read_file(r'C:\Users\larij\.spyder-py3\Korona konkurssit\Kuntarajat.shp')

# Yhdistetään yrityskanta kuntakarttaan

kunnat_merged = pd.merge(kunnat, yrityskanta, on='nimi')

# Lisätään sarake konkursseille

kunnat_merged['konkurssit'] = 0

# Moduuli konkurssien määrän hakemiseksi yhdestä annetusta kunnasta

def hae_kunnan_konkurssit(kunta,raakadata):
    palautettava = 0
    for konkurssi in raakadata:
        if konkurssi['registeredOffice'] == kunta:
            palautettava = palautettava + 1
        else:
            continue
    return palautettava

"""
For-looppi, joka käy jokaisen kunnan yksitellen ja hakee sille äskeisen
moduulin avulla konkurssien määrän
"""

i = 0
for kunta in kunnat_merged['nimi']:
    kunnat_merged['konkurssit'].iloc[i] = hae_kunnan_konkurssit(kunta,konk_data['results'])
    i = i + 1
    
#Tehdään uusi sarake, johon lasketaan konkurssien osuus koko yrityskannasta

kunnat_merged['konkurssien_osuus'] = 0.0

# For-loop, joka käy läpi kaikki kunnat ja lisää 'konkurssien osuus'-sarakkeeseen konkurssiin
# menneiden yritysten %-osuuden koko yrityskannasta

a = 0
for nimi in range(0,310):
    kunnat_merged['konkurssien_osuus'].iloc[a] = ((kunnat_merged['konkurssit'].iloc[a].astype(float)/kunnat_merged['Yrityskanta,q2/2019'].iloc[a].astype(float))*100)
    a = a + 1
    
#Tehdään kartta
    
# Muuttuja, jonka perusteella kunnat visualisoidaan
    
muuttuja_suht = 'konkurssien_osuus'

muuttuja_abs = 'konkurssit'

# Asetetaan visualisoinnin raja-arvot

mmin, mmax = 0.0, 0.6

# Tehdään valmistelut

fig, ax = plt.subplots(1, figsize = (9, 12))

# Kartan plottaus

kunnat_merged.plot(column=muuttuja_suht, cmap='Reds',linewidth=0.8,ax=ax,edgecolor='0.8')

# Poistetaan x- ja y-akselien selitteet

ax.axis('off')

# Lisätään otsikko

ax.set_title('Konkurssien %-osuus yrityskannasta kunnissa 1.1.2020 lähtien. Uusin data: ' + str(eilinen) + '.', fontdict={'fontsize': '12', 'fontweight' : '3'})

# Lähdeviittaus

ax.annotate('Lähde: PRH ja MML. Konkurssien määrä yht: ' + str(konk_sum), xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=11, color='#555555')

# Create colorbar as a legend

sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=mmin, vmax=mmax))

# empty array for the data range

sm._A = []

# add the colorbar to the figure

cbar = fig.colorbar(sm)

# Tallennetaan kartta

fig.savefig('korona_konkurssit_2020.png', dpi=300)

# Datan vieminen exceliin
kunnat_merged.to_excel('kunnatjakonkat.xlsx')