#imports

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import numpy as np

#=================================================================================================================================================================
#functions to extract data using web scrapping
#=================================================================================================================================================================


def date_time(table_cells):
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    out=''.join([booster_version for i,booster_version in enumerate( table_cells.strings) if i%2==0][0:-1])
    return out

def landing_status(table_cells):
    out=[i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass=unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass=mass[0:mass.find("kg")+2]
    else:
        new_mass=0
    return new_mass


def extract_column_from_header(row):
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()

    colunm_name = ' '.join(row.contents)

    # Filter the digit and empty names
    if not(colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name

#source
static_url="https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

# Request the Falcon9 Launch Wiki page
response=requests.get(static_url, headers=headers)

# Check status
print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify()[0:200])

#DATA extraction

# Find all tables on the page
tables=soup.find_all("table", "wikitable")

print("Number of tables found:", len(tables))

first_table=tables[0]

header_row=first_table.find("tr")

header_cells=header_row.find_all("th")

# Use helper function to clean names
column_names=[extract_column_from_header(cell) for cell in header_cells]

print("Column names:", column_names)


#extract data from 3rd table
target_table=tables[2]
print(column_names)

for th in target_table.find_all("th"):
    name=extract_column_from_header(th)
    # Append only non-empty names
    if name is not None and len(name)>0:
        column_names.append(name)

print("Extracted column names:", column_names)


#Create a dataframe from HTML table
launch_dict= dict.fromkeys(column_names)

# Remove an irrelvant column
del launch_dict['Date and time ( )']

# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]


extracted_row=0
#Extract each table
for table_number,table in enumerate(soup.find_all('table',"wikitable plainrowheaders collapsible")):
   # get table row
    for rows in table.find_all("tr"):
        #check to see if first table heading is as number corresponding to launch a number
        if rows.th:
            if rows.th.string:
                flight_number=rows.th.string.strip()
                flag=flight_number.isdigit()
        else:
            flag=False
        row=rows.find_all('td')

        if flag:
            extracted_row+=1
            datatimelist=date_time(row[0])

            date=datatimelist[0].strip(',')
            launch_dict['Date'].append(date)

            time=datatimelist[1]
            launch_dict['Time'].append(time)

            bv=booster_version(row[1])
            if not(bv):
                bv=row[1].a.string if row[1].a else None
            # print(bv)
            launch_dict['Version Booster'].append(bv)

            launch_site=row[2].a.string if row[2].a else None
            launch_dict['Launch site'].append(launch_site)

            payload=row[3].a.string if row[3].a else None
            launch_dict['Payload'].append(payload)

            payload_mass=get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)

            orbit=row[5].a.string if row[5].a else None
            launch_dict['Orbit'].append(orbit)

            customer=row[6].a.string if row[6].a else None
            launch_dict['Customer'].append(customer)

            launch_outcome=list(row[7].strings)[0] if row[7] else None
            launch_dict['Launch outcome'].append(launch_outcome)

            booster_landing=landing_status(row[8]) if row[8] else None
            launch_dict['Booster landing'].append(booster_landing)

            launch_dict['Flight No.'].append(flight_number)


df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items()})

df.head()
df.to_csv('spacex_web_scraped.csv', index=False)

#=================================================================================================================================================================
#  DATA extraction using PANDAS read_csv()
#=================================================================================================================================================================

df1=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")

#=================================================================================================================================================================
