# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 14:08:33 2020

@author: Lari Jaakkola
"""

# Tässä skriptissä tehdään automaattisesti päivittyvä graafi koko vuoden 2020 konkursseista
# Algoritmi muokataan maaliskuun konkursseja käsittelevästä scriptistä

import requests
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
from datetime import timedelta

url = 'https://avoindata.prh.fi/tr/v1/publicnotices?totalResults=true&maxResults=1000&resultsFrom=0&entryCode=KONALK&noticeRegistrationFrom=2020-01-01'

konk_data = requests.get(url).json()

print('Total results: ', konk_data['totalResults'])

# ensin määritellään se mistä päivästä määrittelyn halutaan lähtevän liikkeelle

#alkupvm = date(2020,3,1)

# Tehdään timedelta halutusta ajasta

start_date = date(2020, 1, 1)

end_date = date.today()

delta = timedelta(days=1)

# Tehdään eilinen päivä

eilinen = end_date - timedelta(days=1)

# muutetaan raakadatan päivämäärät datatime-objekteiksi

for yritys in konk_data['results']:
    yritys['registrationDate'] = datetime.strptime(yritys['registrationDate'], '%Y-%m-%d').date()

# Päivät listaan
    
pvat_listassa = []

for i in range((end_date - start_date).days):
    pvat_listassa.append(start_date + i*delta)

# Määritellään graafin leveys (päivien lukumäärä)

graph_leveys = []

aloitus = 1
for paiva in range(0,len(pvat_listassa)):
    graph_leveys.append(aloitus)
    aloitus = aloitus + 1

# automaattinen palkkien korkeuksien määrittely

# haetaan konkurssit

maalis_konkurssit = []

def hae_kys_pvan_konkurssit(haettava_pva, raakadata):
    palautettava = 0
    for konkurssi in raakadata:
        if konkurssi['registrationDate'] == haettava_pva:
            palautettava = palautettava + 1
        else:
            continue
    return palautettava

for paiva in pvat_listassa:
    maalis_konkurssit.append(hae_kys_pvan_konkurssit(paiva,konk_data['results']))

# Diagrammin teko
    
kuukaudet =  ['Tammikuu','Helmikuu','Maaliskuu','Huhtikuu','Toukokuu','Kesäkuu','Heinäkuu','Elokuu','Syyskuu','Lokakuu']
    
plt.figure(figsize=(20,5))

plt.bar(graph_leveys, maalis_konkurssit, width=0.3, bottom=None, align='center', data=None, color='darkorange')

# Add title and axis names
plt.title('Konkurssiin asetetut yritykset Suomessa vuoden 2020 aikana. Yksi palkki kuvastaa yhden päivän konkursseja. Lähde: PRH. Uusin data: '+str(eilinen),fontsize=10)
plt.xlabel('Kuukausi', fontsize = 10)
plt.ylabel('Uusien konkurssien lukumäärä / päivä', fontsize=10)

# Limits for the Y axis
plt.ylim(0,20)

plt.xticks(graph_leveys)

plt.xticks(ticks = (15,45,75,105,135,165,195,225,255,285),labels = (kuukaudet))

plt.savefig(fname='Konk_2020_autom.png')