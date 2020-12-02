#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 18:51:24 2020

@author: fouad
"""

import requests
from tqdm import tqdm
import json




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
    
def write_json(data, filename):
    '''
    FUNCTION TO WRITE A JSON FILE 
    '''
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
# method was found on api webstie



## get chicago data from endpoint


data = []


######### CHICAGO - USA ##########

print("Fetching Chicago City - USA crime data:")
for year in tqdm(range(2018,2021), desc = "Progress per year"):
    for month in range(1,13):
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            if (year == 2020 and month > 10):
                break
            for day in range(1,32):
                if month < 10:
                    if day < 10:
                        date = str(year)+"-0"+str(month)+"-0"+str(day)
                        base_url = " https://data.cityofchicago.org/resource/ijzp-q8t2.json?date="+date+"T00:00:00.000"
                        response = requests.get(base_url).json()
                        data.append(response)
                    else:
                        date = str(year)+"-0"+str(month)+"-"+str(day)
                        base_url = " https://data.cityofchicago.org/resource/ijzp-q8t2.json?date="+date+"T00:00:00.000"
                        response = requests.get(base_url).json()
                        data.append(response)
                else:
                    if day < 10:
                        date = str(year)+"-"+str(month)+"-0"+str(day)
                        base_url = " https://data.cityofchicago.org/resource/ijzp-q8t2.json?date="+date+"T00:00:00.000"
                        response = requests.get(base_url).json()
                        data.append(response)
                    else:
                        date = str(year)+"-"+str(month)+"-"+str(day)
                        base_url = " https://data.cityofchicago.org/resource/ijzp-q8t2.json?date="+date+"T00:00:00.000"
                        response = requests.get(base_url).json()
                        data.append(response) 
filename = "USA_chicago_crime_data.json"
print("Creating json file", filename)
write_json(data, filename)

# cleaning up chicago JSON file
print("Cleaning file ", filename)
data = open_json("USA_chicago_crime_data.json")

chicago_crime_data = []
for items in data:
    for item in items:
        data_set = {
            "date" : item["date"],
            "offense_type" : item["primary_type"],
            "year" : item["year"]}
        chicago_crime_data.append(data_set)

print("Creating json file", filename)     
write_json(chicago_crime_data,filename)



######### DALLAS CITY - USA ##########
data = []
print("\nFetching crime data from Dallas - USA")
for year in tqdm(range(2018,2021), desc = "\nProgress per year"):
    base_url = "https://www.dallasopendata.com/resource/qv6i-rri7.json?year1="+str(year)
    response = requests.get(base_url).json()
    data.append(response) 
    
filename = "USA_dallas_crime_data.json"
print("\nCreating json file", filename)
write_json(data, filename)

data = open_json(filename)
print("Cleaning file", filename)
dallas_crime_data = []
# unpacking data from list
for items in data:
    for item in items:
        data_set = {
            "year" : item["eyear"],
            "month" : item["emonth"],
            "offense_type" : item["nibrs_crime"]}
        dallas_crime_data.append(data_set)
        
write_json(dallas_crime_data, filename)


######## SAN FRANCISCO CITY - USA ##########
data = []
print("Fetching crime data from San Fransico - USA")
for year in tqdm(range(2018,2021), desc = "\nProgress per year"):
    base_url = "https://data.sfgov.org/resource/wg3w-h783.json?incident_year="+str(year)
    response = requests.get(base_url).json()
    data.append(response) 
    
filename = "USA_sanfrancisco_crime_data.json"
print("\nCreating json file", filename)
write_json(data, filename)

data = open_json(filename)
print("Cleaning file", filename)
sf_crime_data = []
# unpacking data from list
for items in data:
    for item in items:
        data_set = {
            "year" : item["incident_year"],
            "date" : item["incident_date"],
            "offense_type" : item["incident_description"]
            }
        sf_crime_data.append(data_set)

write_json(sf_crime_data, filename)   


