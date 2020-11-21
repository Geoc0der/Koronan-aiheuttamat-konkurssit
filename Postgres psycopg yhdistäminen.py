# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 20:29:12 2020

@author: larij
"""


# Tässä scriptissä yhdistetään rajapinta postgres-tietokantaan psycopg:n avulla
# ja viedä sinne Tampereella vuonna 2020 perustetut yritykset
# Tietokantataulu on tehty valmiiksi

# Tuodaan tarvittavat kirjastot työtilaan

import psycopg2
import requests

# Api-osoite konkurssidatalle

url = 'https://avoindata.prh.fi/bis/v1?totalResults=true&resultsFrom=0&registeredOffice=Tampere&companyRegistrationFrom=2020-01-01'

# Asetetaan json-data muuttujaan

aloit_data = requests.get(url).json()

try:

    connection = psycopg2.connect(user="xxxx",
                                  password="xxxx",
                                  host="xxxx",
                                  database="xxxx")
    
    # Alustetaan kursori
    
    cursor = connection.cursor()


    # Viedään data cursorin avulla tietokantaan käyttämällä executemany-funktiota

    cursor.executemany("""INSERT INTO tietokantataulu (businessId,name,registrationDate,companyForm,detailsUri) VALUES (%(businessId)s,%(name)s,%(registrationDate)s,%(companyForm)s,%(detailsUri)s)""", aloit_data['results'])

    # Vahvistetaan tietokannan päivitys commit-toiminnolla

    connection.commit()

# Tarkistetaan yhteys poikkeuksien varalta

except(Exception, psycopg2.DatabaseError) as error:
    print('Error while creating Postgres table', error)
    
finally:
    # Suljetaan tietokantayhteys
    if(connection):
        cursor.close()
        connection.close()
        print('Postgres connection is closed')
