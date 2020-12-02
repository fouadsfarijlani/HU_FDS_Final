#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:00:52 2020

@author: fouad
"""



import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import selenium
import time
import json



# web driver location
path = "/Users/fouad/Desktop/HU - Master Data Driven Design/Block A/Fundamentals of Data Science/Final/chromedriver"

# using chrome as our browser
driver = webdriver.Chrome(path)

url = "https://www.cbs.nl/nl-nl/visualisaties/welvaart-in-coronatijd/veiligheid/"

driver.get(url)

def open_collapse_tab(driver, id, name):
    '''
    OPEN COLLAPSE TABLES USING SELENIUM

    Parameters
    ----------
    driver : CHROME WEBDRIVER
        DESCRIPTION.
    id : STR
        ID OF HTML CLASS.
    name : STR
        NAME OF HTML CLASS INSIDE CONTAINER.

    Returns
    -------
    None.

    '''
    container = driver.find_element_by_id(id)
    link = container.find_element_by_class_name(name)
    link.click()

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

# function to write JSON file    
def write_json(data, filename):
    '''
    FUNCTION TO WRITE A JSON FILE 
    '''
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)



open_collapse_tab(driver, "datatable-container-highcharts-cor-veiligheid-woninginbraken", "if-collapsed")
open_collapse_tab(driver, "datatable-container-highcharts-cor-veiligheid-misdrijven","if-collapsed")
open_collapse_tab(driver, "datatable-container-highcharts-cor-veiligheid-overlast-lijnen", "if-collapsed")




page = driver.page_source
time.sleep(2)
soup = BeautifulSoup(page, "html.parser")

# safety_and_security = get_data(page, "datatable-highcharts-cor-veiligheid-misdrijven")
# print(safety_and_security)

# safety crime
# id = datatable-highcharts-cor-veiligheid-misdrijven

overview = soup.find(id = "datatable-highcharts-cor-veiligheid-misdrijven")
body = overview.find("tbody")
results = body.findAll("tr")
safety_and_security = []
for item in results:
    month = item.find(scope = ["row"]).get_text()
    number = item.find("td").get_text()
    
    crime_set = {
        "Month": month,
        "Number" : number}
    
    safety_and_security.append(crime_set)
    
filename = "NL_safety_and_security_crimes.json"
print("creating file",filename)
write_json(safety_and_security, filename)

# break ins
# id = datatable-highcharts-cor-veiligheid-woninginbraken

overview = soup.find(id = "datatable-highcharts-cor-veiligheid-woninginbraken")
body = overview.find("tbody")
results = body.findAll("tr")
break_ins = []
for item in results:
    month = item.find(scope = ["row"]).get_text()
    number = item.find("td").get_text()
    
    crime_set = {
        "Month": month,
        "Number" : number}
    
    break_ins.append(crime_set)

filename = "NL_break_ins_crimes.json"
print("creating file",filename)
write_json(break_ins, filename)

# Registered nuisance
# id = datatable-highcharts-cor-veiligheid-overlast-lijnen

overview = soup.find(id = "datatable-highcharts-cor-veiligheid-overlast-lijnen")
body = overview.find("tbody")
results = body.findAll("tr")
# print(results)

registered_nuisance = []
for item in results:
    month = item.find(scope = ["row"]).get_text()
    numbers = item.findAll("td")
    # print(month)
    n = []
    c = 0
    for number in numbers:
        year = ""
        if c == 0:
            year = "2020"
        elif c == 1:
            year = "2019"
        elif c == 2:
            year = "2018"
        else:
            year = "2017"
        n.append(number.get_text() + "-" + year)
        c += 1 
    crime_set = {
        "Month": month,
        "Number" : n,
        }
    
    registered_nuisance.append(crime_set)

filename = "NL_registered_nuisance_crime.json"
print("creating file",filename)
write_json(registered_nuisance, filename)

### fixing data

data = open_json("NL_registered_nuisance_crime.json")
nl_rn = []
for items in data:
    month = items["Month"]
    for item in items["Number"]:
        year = item[6:11].replace("-","")
        number = item[0:6]. replace(",","").replace("-","")
        data_set = {"Month" : month,
                    "Year" : year,
                    "Number": number}
        nl_rn.append(data_set)
        
print("Fixing dataset..")
write_json(nl_rn, filename)

driver.quit()





