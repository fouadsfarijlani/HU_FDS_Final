#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 16:02:59 2020

@author: fouad
"""

import requests
import json
from tqdm import tqdm
import time


def write_json(data, filename):
    '''
    FUNCTION TO WRITE A JSON FILE 
    '''
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
        
def open_json(filename):
    '''
    FUNCTION TO OPEN A JSON FILE

    Parameters
    ----------
    filename : TYPE STRING
        DESCRIPTION: NAME OF THE FILE TO BE OPENED.

    Returns
    -------
    data : TYPE DICT
        DESCRIPTION RETURN THE DATA FILE IN A DICT TYPE .

    '''
    with open(filename) as json_file:
        data = json.load(json_file)
        return data
    
    

url_uk_forces = "https://data.police.uk/api/forces"

force = ""

print("Fetching data from UK Police")
time.sleep(0.5)

# url_uk_crime = "https://data.police.uk/api/crimes-no-location?"

response = requests.get(url_uk_forces)
list_of_forces = response.json()


crimes_uk = []
for year in tqdm(range(2018,2021), desc = "progressing"):
   for month in range(1,13):  
       if year == 2020 and month >= 9:
           break
       # print("Fetching data for month", month, "year", year)
       for item in list_of_forces: 
            date = str(year)+"-"+str(month)
            force = item["id"]
            # print("getting data from",item["name"], "...")
            url_uk_crime = "https://data.police.uk/api/crimes-no-location?category=all-crime&force="+force+"&date="+date
            
            response = requests.get(url_uk_crime).json()
            
            crimes_uk.append(response)
            
          

# saving data taken from endpoint
filename = "uk_crime_data.json"
print("Creating JSON file", filename)
write_json(crimes_uk,filename)

# removing redundacy from data
data = open(filename)
data = json.load(data)

uk_crime_data = []

for items in data:
    for item in items:
        uk_crime = {
        "Category": item["category"],
        "Month" : item["month"]
            }
        uk_crime_data.append(uk_crime)

print("removing redundant data from",filename)
write_json(uk_crime_data, filename)

    


