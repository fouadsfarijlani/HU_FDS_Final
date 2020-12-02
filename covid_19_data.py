#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 18:42:51 2020

@author: fouad
"""

import requests
import json
import os
from tqdm import tqdm, tnrange

# function to open JSON file
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

# base URL for covid-19 endpoint
# documentation https://covid19tracking.narrativa.com/index_en.html

base_url = "https://api.covid19tracking.narrativa.com/api/"

# creating jSON FILES with date parameters
# dividing files in days for easier processing

for m in tqdm(range(1,10), desc = "Getting Covid-19 Data from end point"):
    if m == 1:
        for d in range(24,32):
            # print("getting data for month",m,"day", d)
            if d < 10:
                covid_data = []
                day = "2020-0"+str(m)+"-0"+str(d)
                url = base_url+day
                response = requests.get(url).json()
                covid_data.append(response)
                
                filename = "covid19_data_"+day+".json"
                # print("creating json file", filename, "...")
                
                write_json(covid_data, filename)
                
            else:
                covid_data = []
                day = "2020-0"+str(m)+"-"+str(d)
                url = base_url+day
                response = requests.get(url).json()
                covid_data.append(response)
                
                filename = "covid19_data_"+day+".json"
                # print("creating json file", filename, "...")
                
                write_json(covid_data, filename)
                
    
    elif m == 3 or m == 5 or m == 7 or m == 8:
        for d in range(1,32):
            # print("getting data for month",m,"day", d)
            if d < 10:
                covid_data = []
                day = "2020-0"+str(m)+"-0"+str(d)
                url = base_url+day
                response = requests.get(url).json()
                covid_data.append(response)
                
                filename = "covid19_data_"+day+".json"
                # print("creating json file", filename, "...")
                
                write_json(covid_data, filename) 
                
            else:
                covid_data = []
                day = "2020-0"+str(m)+"-"+str(d)
                url = base_url+"2020"+"-0"+str(m)+"-"+str(d)
                response = requests.get(url).json()
                covid_data.append(response)
                
                filename = "covid19_data_"+"2020"+"-0"+str(m)+"-"+str(d)+".json"
                # print("creating json file", filename, "...")
                
                write_json(covid_data, filename) 
                

    elif m == 4 or m == 6 or m == 9:
        for d in range(1,31):
            # print("getting data for month",m,"day", d)
            if d < 10:
                covid_data = []
                day = "2020-0"+str(m)+"-0"+str(d)
                url = base_url+day
                response = requests.get(url).json()
                covid_data.append(response)
                
                filename = "covid19_data_"+day+".json"
                # print("creating json file", filename, "...")
                
                write_json(covid_data, filename)
                    
            else:
                covid_data = []
                day = day = "2020-0"+str(m)+"-"+str(d)
                url = base_url+day
                response = requests.get(url).json()
                covid_data.append(response)
                
                filename = "covid19_data_"+day+".json"
                # print("creating json file", filename, "...")
               
                write_json(covid_data, filename)
        
    else:
        for d in range(1,29):
            if d < 10:
                covid_data = []
                day = "2020-0"+str(m)+"-0"+str(d)
                # print("getting data for month",m,"day", d)
                url = base_url+day
                response = requests.get(url).json()
                covid_data.append(response)
            
                filename = "covid19_data_"+day+".json"
                # print("creating json file", filename, "...")
                
                write_json(covid_data, filename)
                    
            else:
                covid_data = []
                day = day = "2020-0"+str(m)+"-"+str(d)
                # print("getting data for month",m,"day", d)
                url = base_url+day
                response = requests.get(url).json()
                covid_data.append(response)
            
                filename = "covid19_data_"+day+".json"
                # print("creating json file", filename, "...")
                
                write_json(covid_data, filename)
                

# extracting necessary data from JSON files created
covid_data = []
for m in tqdm(range(1,10),desc = "Extracting data from JSON files"):
    if m == 1:
        for d in range(24,31):
            day = "2020-0" + str(m) + "-" + str(d) 
            filename = "covid19_data_"+day+".json"
            data = open_json(filename)
            # print("processing file: "+filename)
            for items in data:
                for key, item in items["dates"][day]["countries"].items():
                    covid_dict = {
                        "Country" : item["name"],
                        "Cases": item["today_new_confirmed"],
                        "date": day}
                    covid_data.append(covid_dict)
                    
    elif m == 3 or m == 5 or m == 7 or m == 8:
        for d in range(1,32):
            if d < 10:
                day = "2020-0" + str(m) + "-0" + str(d)
                filename = "covid19_data_"+day+".json"
                data = open_json(filename)
                # print("processing file: "+filename)
                for items in data:
                    for key, item in items["dates"][day]["countries"].items():
                
                        covid_dict = {
                            "Country" : item["name"],
                            "Cases": item["today_new_confirmed"],
                            "date": day}
                        covid_data.append(covid_dict)
                        
            else:
                day = "2020-0" + str(m) + "-" + str(d)
                filename = "covid19_data_"+day+".json"
                data = open_json(filename)
                # print("processing file: "+filename)
                for items in data:
                    for key, item in items["dates"][day]["countries"].items():
                
                        covid_dict = {
                            "Country" : item["name"],
                            "Cases": item["today_new_confirmed"],
                            "date": day}
                        covid_data.append(covid_dict)
    
    elif m == 4 or m == 6 or m == 9:
        for d in range(1,31):
            if d < 10:
                day = "2020-0" + str(m) + "-0" + str(d)
                filename = "covid19_data_"+day+".json"
                data = open_json(filename)
                # print("processing file: "+filename)
                for items in data:
                    for key, item in items["dates"][day]["countries"].items():
                
                        covid_dict = {
                            "Country" : item["name"],
                            "Cases": item["today_new_confirmed"],
                            "date": day}
                        covid_data.append(covid_dict)
                        
            else:
                day = "2020-0" + str(m) + "-" + str(d)
                filename = "covid19_data_"+day+".json"
                data = open_json(filename)
                # print("processing file: "+filename)
                for items in data:
                    for key, item in items["dates"][day]["countries"].items():
                
                        covid_dict = {
                            "Country" : item["name"],
                            "Cases": item["today_new_confirmed"],
                            "date": day}
                        covid_data.append(covid_dict)
                        
    else:
        for d in range(1,28):
            if d < 10:
                day = "2020-0" + str(m) + "-0" + str(d)
                filename = "covid19_data_"+day+".json"
                data = open_json(filename)
                # print("processing file: "+filename)
                for items in data:
                    for key, item in items["dates"][day]["countries"].items():
                
                        covid_dict = {
                            "Country" : item["name"],
                            "Cases": item["today_new_confirmed"],
                            "date": day}
                        covid_data.append(covid_dict)
                        
            else:
                day = "2020-0" + str(m) + "-" + str(d)
                filename = "covid19_data_"+day+".json"
                data = open_json(filename)
                # print("processing file: "+filename)
                for items in data:
                    for key, item in items["dates"][day]["countries"].items():
                
                        covid_dict = {
                            "Country" : item["name"],
                            "Cases": item["today_new_confirmed"],
                            "date": day}
                        covid_data.append(covid_dict)

# new consolidated JSON file 
filename = "covid19_data.json"
print("Creating a new JSON File:", filename)
write_json(covid_data, filename)                    

# remvoing unecessary data
for m in tqdm(range(1,10), desc = "Removing uncessary files"):
    # print("Cleaning up data for month:", m)
    if m == 1:
        for d in range(24,32):
            if d < 10:
                day = "2020-0"+str(m)+"-0"+str(d)
                filename = "covid19_data_"+day+".json"
                # print("Removing JSON file:",filename)
                os.remove(filename)
            else:
                day = "2020-0"+str(m)+"-"+str(d)
                filename = "covid19_data_"+day+".json"
                # print("Removing JSON file:",filename)
                os.remove(filename)
    elif m == 3 or m == 5 or m == 7 or m == 8:
        for d in range(1,32):
            if d < 10:
                day = "2020-0"+str(m)+"-0"+str(d)
                filename = "covid19_data_"+day+".json"
                # print("Removing JSON file:",filename)
                os.remove(filename)
            else:
                day = "2020-0"+str(m)+"-"+str(d)
                filename = "covid19_data_"+day+".json"
                # print("Removing JSON file:",filename)
                os.remove(filename)
    elif m == 4 or m == 6 or m == 9:
        for d in range(1,31):
            if d < 10:
                day = "2020-0"+str(m)+"-0"+str(d)
                filename = "covid19_data_"+day+".json"
                # print("Removing JSON file:",filename)
                os.remove(filename)
            else:
                day = "2020-0"+str(m)+"-"+str(d)
                filename = "covid19_data_"+day+".json"
                # print("Removing JSON file:",filename)
                os.remove(filename)
    else:
        for d in range(1,29):
            if d < 10:
                day = "2020-0"+str(m)+"-0"+str(d)
                filename = "covid19_data_"+day+".json"
                # print("Removing JSON file:",filename)
                os.remove(filename)
            else:
                day = "2020-0"+str(m)+"-"+str(d)
                filename = "covid19_data_"+day+".json"
                # print("Removing JSON file:",filename)
                os.remove(filename)
    
    

