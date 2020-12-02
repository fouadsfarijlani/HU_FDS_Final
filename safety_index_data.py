#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 09:39:43 2020

@author: fouad
"""

import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

def write_json(data, filename):
    '''
    FUNCTION TO WRITE A JSON FILE 
    '''
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

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
    
print("fetching Safety Index Data per year:\n")

time.sleep(0.2)

safety_index_data = []
for year in tqdm(range(2018,2021)):
    url = "https://www.numbeo.com/crime/rankings.jsp?title="+str(year)+"&displayColumn=1"  
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find(id = "t2")
    body = table.findAll("tr")
    
    for item in body:
        data = item.get_text().strip()
        data = data.replace("\n", " - ")
        dataset = {"Year" : str(year),
                    "Data" : data}
        safety_index_data.append(dataset)
safety_index_data.pop(0)
    
filename = "Safety_index_data.json"
print("\n\ncreating json file")
write_json(safety_index_data, filename)
print("json file created:", filename)




    