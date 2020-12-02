#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 20:23:22 2020

@author: fouad
"""

import json
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
# import plotly.graph_objects as go
import numpy as np


def open_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data
def write_json(data, filename):
    '''
    FUNCTION TO WRITE A JSON FILE 
    '''
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
  
    
# ##### COVID-19 DATA ####

print("Processing data for COVID-19..")
# JSON filename 
filename = "covid19_data.json"

# load json file into a df
df_covid19 = pd.read_json(filename)

# select uk, usa, nl from df 
df_covid19 = df_covid19[(df_covid19["Country"] == "United Kingdom") | (df_covid19["Country"] == "Netherlands") | (df_covid19["Country"] == "US") ].copy()

# sort countries in an ascending order
df_covid19 = df_covid19.sort_values(by = "date", ascending=True)

pd.to_datetime(df_covid19["date"])

### UK CRIME DATA ###
print("processing data for UK..")
# JSON filename
filename = "uk_crime_data.json"

# loading json file into a df
df_uk = pd.read_json(filename)

# creating a new column for every crime count is 1
df_uk["Incident_count"] = 1

# changing column Category to incindent_type
df_uk["Incident_type"] = df_uk["Category"]

# changing column Month to Date
df_uk["Date"] = df_uk["Month"]

# droping unecessary columns
df_uk.drop(["Category", "Month"], axis = 1, inplace=True)   

# grouping the sum of every crime by category and month
df_uk = df_uk.groupby(["Date", "Incident_type"]).sum().reset_index()

# creating a column for country name
df_uk["Place"] = "UK"


### USA CRIME DATA ###

## DC CITY ##

print("Processing data for USA - DC CITY...")
# loading USA DC csv's into seperate data frames
df_usa_dc_2018 = pd.read_csv("USA_dc_crime_2018.csv")
df_usa_dc_2019 = pd.read_csv("USA_dc_crime_2019.csv")
df_usa_dc_2020 = pd.read_csv("USA_dc_crime_2020.csv")

# combining dataframes into a temporary df
df_temp = [df_usa_dc_2018, df_usa_dc_2019, df_usa_dc_2020]

# concatinating data frames
df_usa_dc = pd.concat(df_temp)

# releasing unecessary df from memory
del df_temp, df_usa_dc_2018, df_usa_dc_2019, df_usa_dc_2020

# cleaning data
df_usa_dc.drop(["X","Y","CCN", "SHIFT", "METHOD", "BLOCK", "XBLOCK", "YBLOCK", "WARD", "ANC", "DISTRICT", "PSA", "NEIGHBORHOOD_CLUSTER", "BLOCK_GROUP", "CENSUS_TRACT", "VOTING_PRECINCT", "LATITUDE", "LONGITUDE", "BID", "START_DATE", "END_DATE", "OBJECTID", "OCTO_RECORD_ID" ],axis=1, inplace=True)

# changing REPORT_DAT type to str and triming spaces
df_usa_dc["REPORT_DAT"] = df_usa_dc["REPORT_DAT"].astype(str)
df_usa_dc["REPORT_DAT"] = df_usa_dc["REPORT_DAT"].str[:10]
df_usa_dc["REPORT_DAT"] = df_usa_dc["REPORT_DAT"].str.strip()

# create a year column
df_usa_dc["Year"] =  df_usa_dc["REPORT_DAT"].str[:4]

# create a month column
df_usa_dc["Month"] = df_usa_dc["REPORT_DAT"].str[5:7]

# combining month and year into a single column
df_usa_dc["Date"] = df_usa_dc["Year"]+"-"+df_usa_dc["Month"]

# changing column name OFFENSE to Offense_type

df_usa_dc["Incident_type"] = df_usa_dc["OFFENSE"]

# removing unecessary column
df_usa_dc.drop(["REPORT_DAT", "Year", "Month", "OFFENSE"], axis = 1, inplace=True)

# creating a new column for every crime count is 1
df_usa_dc["Incident_count"] = 1

# calculating
df_usa_dc = df_usa_dc.groupby(["Date", "Incident_type"]).sum().reset_index()


# creating column for place
df_usa_dc["Place"] = "USA - DC"


## HOUSTON CITY ##

print("Processing data for USA - HOUSTON CITY...")
#loading USA Houston csv into seperate data frames
df_usa_houston = pd.read_csv("USA_houston_crime_data.csv")

# converting date to string
df_usa_houston["Date"] = df_usa_houston["Date"].astype(str)

# creting year column
df_usa_houston["Year"] = df_usa_houston["Date"].str[:4]

# creating month column
df_usa_houston["Month"] = df_usa_houston["Date"].str[5:7]

# changing column name
df_usa_houston["Incident_type"] = df_usa_houston["Offense Type"]

df_usa_houston["Incident_count"] = df_usa_houston["Offenses"]

# droping date column and creating a new one
df_usa_houston.drop(["Date", "Offense Type", "Offenses"], axis = 1 , inplace=True)

# creating a new date column
df_usa_houston["Date"] = df_usa_houston["Year"] + "-" + df_usa_houston["Month"]

# calculating 
df_usa_houston = df_usa_houston.groupby(["Date", "Incident_type"]).sum().sort_values(by = "Date").reset_index()

#creating a column for place
df_usa_houston["Place"] = "USA - HOUSTON"


## PHILADELPHIA CITY ##

print("Processing data for USA - PHILADELPHIA CITY...")

# loading USA Philadelphia csv into seperate data frames
df_usa_phil = pd.read_csv("USA_philadelphia_crime_data_2018_2020.csv")

# removing unecessary columns
df_usa_phil.drop(["objectid", "dc_dist", "psa", "dispatch_date_time", "dispatch_time", "hour_", "dc_key", "location_block", "ucr_general", "point_x", "point_y", "lat", "lng"],axis=1, inplace=True)

# value for every crime = 1
df_usa_phil["Incident_count"] = 1

# pd.to_datetime(df_usa_phil["dispatch_date"],format = "d%m%Y")

# converting dispatch_date to str
df_usa_phil["dispatch_date"] = df_usa_phil["dispatch_date"].astype(str)

# creating year column
df_usa_phil["year"] = df_usa_phil["dispatch_date"].str[:4]

# creating month column
df_usa_phil["month"] = df_usa_phil["dispatch_date"].str[5:7]

# creating date column
df_usa_phil["Date"] = df_usa_phil["year"]+"-"+df_usa_phil["month"]

# creating new column 
df_usa_phil["Incident_type"] = df_usa_phil["text_general_code"]

# droping unecessary columns
df_usa_phil.drop(["dispatch_date", "year", "month", "text_general_code"], axis=1, inplace=True)

# calculating
df_usa_phil = df_usa_phil.groupby(["Date", "Incident_type"]).sum().sort_values(by= "Date", ascending=True).reset_index()

# creating column for place
df_usa_phil["Place"] = "USA - PHILADELPHIA"


## CHICAGO CITY ##
print("Processing Data for USA - CHICAGO CITY...")

# loading USA Philadelphia csv into seperate data frames
df_usa_chicago = pd.read_json("USA_chicago_crime_data.json")

# casting date and year column to str
df_usa_chicago["date"] = df_usa_chicago["date"].astype(str)
df_usa_chicago["year"] = df_usa_chicago["year"].astype(str)

# getting month from date column
df_usa_chicago["month"] = df_usa_chicago["date"].str[5:7]

# droping old date column and creating a new one
df_usa_chicago.drop(["date"], axis = 1, inplace=True)
df_usa_chicago["Date"] = df_usa_chicago["year"]+"-"+df_usa_chicago["month"]
df_usa_chicago["Incident_type"] = df_usa_chicago["offense_type"]
df_usa_chicago.drop(["year", "month", "offense_type"], axis = 1, inplace=True)

# creating a count for every column
df_usa_chicago["Incident_count"] = 1

# calculating
df_usa_chicago = df_usa_chicago.groupby(["Date", "Incident_type"]).sum().sort_values(by="Date", ascending=True).reset_index()

# creating column for place
df_usa_chicago["Place"] = "USA - CHICAGO"




## DALLAS CITY ##

print("Processing data for USA - DALLAS CITY...")

df_usa_dallas = pd.read_json("USA_dallas_crime_data.json")

# casting year column to str
df_usa_dallas["year"] = df_usa_dallas["year"].astype(str)

# replacing month with numbers
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("January", "01")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("February", "02")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("March", "03")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("April", "04")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("May", "05")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("June", "06")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("July", "07")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("August", "08")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("September", "09")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("October", "10")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("November", "11")
df_usa_dallas["month"] = df_usa_dallas["month"].str.replace("December", "12")

# creating date column
df_usa_dallas["Date"] = df_usa_dallas["year"]+"-"+df_usa_dallas["month"]

# changing column name
df_usa_dallas["Incident_type"] = df_usa_dallas["offense_type"]

# dropping unecessary columns
df_usa_dallas.drop(["year", "month", "offense_type"], axis = 1, inplace=True)

  # creating a count for every column
df_usa_dallas["Incident_count"] = 1

# calculating
df_usa_dallas = df_usa_dallas.groupby(["Date", "Incident_type"]).sum().sort_values(by = "Date", ascending=True).reset_index()

# creating column for place
df_usa_dallas["Place"] = "USA - DALLAS"


## SAN FRANCISCO CITY ##

print("Processing data for USA - SAN FRANCISCO...")

# loading USA SAN FRANCISCO into df
df_usa_sf = pd.read_json("USA_dallas_crime_data.json")

# casting year to str
df_usa_sf["year"] = df_usa_sf["year"].astype(str)

# replacing month with numbers
df_usa_sf["month"] = df_usa_sf["month"].str.replace("January", "01")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("February", "02")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("March", "03")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("April", "04")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("May", "05")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("June", "06")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("July", "07")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("August", "08")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("September", "09")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("October", "10")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("November", "11")
df_usa_sf["month"] = df_usa_sf["month"].str.replace("December", "12")

# creating column date, incident_type and droping unecessary columns
df_usa_sf["Date"] = df_usa_sf["year"]+"-"+df_usa_sf["month"]
df_usa_sf["Incident_type"] = df_usa_sf["offense_type"]
df_usa_sf.drop(["year", "month", "offense_type"], axis = 1, inplace=True)

  # creating a count for every column
df_usa_sf["Incident_count"] = 1

# calculating
df_usa_sf = df_usa_sf.groupby(["Date", "Incident_type"]).sum().sort_values(by = "Date", ascending = True).reset_index()

# creating column for place
df_usa_sf["Place"] = "USA - SAN FRANCISCO"


# combining data for usa

print("Combining data for USA...")

df_temp = [df_usa_chicago, df_usa_phil,df_usa_dallas, df_usa_houston, df_usa_dc,df_usa_sf]
df_usa = pd.concat(df_temp)
# deleting unecessary df for memory management
del df_temp,df_usa_chicago, df_usa_phil,df_usa_dallas, df_usa_houston, df_usa_dc,df_usa_sf


### NETHERLANDS CRIME DATA ###

print("Processing data for Netherlands..")

## Registered nuisance ##

print("Processing Registered Nuisance data in NL... ")
# loading data set
df_nl_rn = pd.read_json("NL_registered_nuisance_crime.json")

# casting year to str
df_nl_rn ["Year"] = df_nl_rn["Year"].astype(str)

# creating date column
df_nl_rn["Date"] = df_nl_rn["Year"] + "-" + df_nl_rn["Month"]

# creating Incident_count column
df_nl_rn["Incident_count"] = df_nl_rn["Number"]

# creating Incident Type column
df_nl_rn["Incident_type"] = "Registered Nuiance"

# droping unecessary column
df_nl_rn.drop(["Month", "Year", "Number"], axis=1, inplace=True)

# changing date names from dutch to english
df_nl_rn["Date"] = df_nl_rn["Date"].str.replace("januari", "01")
df_nl_rn["Date"] = df_nl_rn["Date"].str.replace("februari", "02")
df_nl_rn["Date"] = df_nl_rn["Date"].str.replace("maart", "03")
df_nl_rn["Date"] = df_nl_rn["Date"].str.replace("april", "04")
df_nl_rn["Date"] = df_nl_rn["Date"].str.replace("mei", "05")
df_nl_rn["Date"] = df_nl_rn["Date"].str.replace("juni", "06")


# calculating
df_nl_rn = df_nl_rn.groupby(["Date", "Incident_type"]).sum().sort_values(by="Date").reset_index()

# creating column place
df_nl_rn["Place"] = "NETHERLANDS"

# BREAK IN##

print("Processing Break in's data in NL... ")

df_nl_bi = pd.read_json("NL_break_ins_crimes.json")

# creating a year column
df_nl_bi["Year"] = df_nl_bi["Month"].str[-4:]

# removing year from month column
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("2015", "").str.strip()
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("2016", "").str.strip()
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("2017", "").str.strip()
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("2018", "").str.strip()
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("2019", "").str.strip()
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("2020", "").str.strip()

# replacing month with numbers
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("januari", "01")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("februari", "02")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("maart", "03")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("april", "04")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("mei", "05")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("juni", "06")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("juli", "07")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("augustus", "08")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("september", "09")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("oktober", "10")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("november", "11")
df_nl_bi["Month"] = df_nl_bi["Month"].str.replace("december", "12")

# replace , in numbers with " and casting to int
df_nl_bi["Number"] = df_nl_bi["Number"].str.replace(",","")
df_nl_bi["Number"] = df_nl_bi["Number"].astype(int)

# creating a new column date
df_nl_bi["Date"] = df_nl_bi["Year"] + "-" + df_nl_bi["Month"]

# creating new column Incident_Type and Incident_Count
df_nl_bi["Incident_type"] = "Break-ins"
df_nl_bi["Incident_count"] = df_nl_bi["Number"]

# droping uncessary columns
df_nl_bi.drop(["Month", "Year","Number"], axis = 1, inplace=True)

# calculating
df_nl_bi = df_nl_bi.groupby(["Date", "Incident_type"]).sum().sort_values(by= "Date", ascending=True).reset_index()

# creating column place
df_nl_bi["Place"] = "NETHERLANDS"

## SAFETY AND SECURITY ##

print("Processing Safety and Secuirty data in NL... ")

df_nl_ss = pd.read_json("NL_safety_and_security_crimes.json")

# creating a year column
df_nl_ss["Year"] = df_nl_ss["Month"].str[-4:]

# removing year from month column
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("2015", "").str.strip()
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("2016", "").str.strip()
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("2017", "").str.strip()
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("2018", "").str.strip()
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("2019", "").str.strip()
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("2020", "").str.strip()

# replacing month with numbers
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("januari", "01")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("februari", "02")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("maart", "03")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("april", "04")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("mei", "05")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("juni", "06")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("juli", "07")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("augustus", "08")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("september", "09")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("oktober", "10")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("november", "11")
df_nl_ss["Month"] = df_nl_ss["Month"].str.replace("december", "12")

# replace , in numbers with " and casting to int
df_nl_ss["Number"] = df_nl_ss["Number"].str.replace(",","")
df_nl_ss["Number"] = df_nl_ss["Number"].astype(int)

# creating a new column date
df_nl_ss["Date"] = df_nl_ss["Year"] + "-" + df_nl_ss["Month"]

# creating new column Incident_Type and Incident_Count
df_nl_ss["Incident_type"] = "Safety and Security"
df_nl_ss["Incident_count"] = df_nl_ss["Number"]

# droping uncessary columns
df_nl_ss.drop(["Month", "Year","Number"], axis = 1, inplace=True)

# calculating
df_nl_ss = df_nl_ss.groupby(["Date", "Incident_type"]).sum().sort_values(by= "Date", ascending=True).reset_index()

# creating column place
df_nl_ss["Place"] = "NETHERLANDS"


## combine NL dfs ## 
df_temp = [df_nl_rn, df_nl_bi, df_nl_ss]
df_nl = pd.concat(df_temp)

# deleting unecessary df for memory management
del df_temp, df_nl_rn, df_nl_bi, df_nl_ss



## COMBINING DATA FOR ALL COUNTRIES

print("Combining all data sets for countries USA, UK, NL..")

df_temp = [df_usa, df_uk, df_nl]
df_incident_all = pd.concat(df_temp)

# removing unecessary data for memory management

del df_temp, df_usa, df_uk, df_nl

# Categorizing Crime sets

# Alcohol related incident
df_incident_all.loc[(df_incident_all["Incident_type"] == "LIQUOR LAW VIOLATION") |
                    (df_incident_all["Incident_type"] == "Public Drunkenness") |
                    (df_incident_all["Incident_type"] == "Liquor Law Violations")|
                    (df_incident_all["Incident_type"] == "DRIVING UNDER THE INFLUENCE")|
                    (df_incident_all["Incident_type"] == "Disorderly Conduct") |
                    (df_incident_all["Incident_type"] == "PUBLIC INTOXICATION")|
                    (df_incident_all["Incident_type"] == "DUI") |
                    (df_incident_all["Incident_type"] == "Disorderly conduct") |
                    (df_incident_all["Incident_type"] == "DISORDERLY CONDUCT") |
                    (df_incident_all["Incident_type"] == "Liquor law violations") |
                    (df_incident_all["Incident_type"] == "Driving under the influence") |
                    (df_incident_all["Incident_type"] == "Drunkenness"), "Incident_category"] = "Alcohol Related Incident" 


# Assault related incident 

df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") &
                    (df_incident_all["Incident_type"] == "ASSAULT") |
                    (df_incident_all["Incident_type"] == "CRIMINAL TRESPASS") |
                    (df_incident_all["Incident_type"] == "KIDNAPPING") |
                    (df_incident_all["Incident_type"] == "Intimidation") |
                    (df_incident_all["Incident_type"] == "Simple assault") |
                    (df_incident_all["Incident_type"] == "INTIMIDATION") |
                    (df_incident_all["Incident_type"] == "Aggravated Assault Firearm") |
                    (df_incident_all["Incident_type"] == "Other Assaults") |
                    (df_incident_all["Incident_type"] == "Aggravated Assault No Firearm") |
                    (df_incident_all["Incident_type"] == "AGG ASSAULT - NFV") |
                    (df_incident_all["Incident_type"] == "SIMPLE ASSAULT") |
                    (df_incident_all["Incident_type"] == "ANIMAL CRUELTY") |
                    (df_incident_all["Incident_type"] == "TRESPASS OF REAL PROPERTY") |
                    (df_incident_all["Incident_type"] == "Aggravated Assault") |
                    (df_incident_all["Incident_type"] == "Kidnapping, abduction") |
                    (df_incident_all["Incident_type"] == "ASSAULT W/DANGEROUS WEAPON") |
                    (df_incident_all["Incident_type"] == "violent-crime"), "Incident_category"] = "Assault related incident"                                                                      


# Damage related incident
df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident") &
                    (df_incident_all["Incident_type"] == "CRIMINAL DAMAGE") |
                    (df_incident_all["Incident_type"] == "PUBLIC PEACE VIOLATION") |
                    (df_incident_all["Incident_type"] == "ARSON") |
                    (df_incident_all["Incident_type"] == "Vandalism/Criminal Mischief") |
                    (df_incident_all["Incident_type"] == "DESTRUCTION/ DAMAGE/ VANDALISM OF PROPERTY") |
                    (df_incident_all["Incident_type"] == "Destruction, damage, vandalism") |
                    (df_incident_all["Incident_type"] == "criminal-damage-arson") |
                    (df_incident_all["Incident_type"] == "Safety and Security") , "Incident_category"] = "Damage related incident"

# Domestic abuse incident

df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident") & (df_incident_all["Incident_category"] != "Damage related incident") &
                    (df_incident_all["Incident_type"] == "OFFENSE INVOLVING CHILDREN") |
                    (df_incident_all["Incident_type"] == "Offenses Against Family and Children") |
                    (df_incident_all["Incident_type"] == "FAMILY OFFENSES, NONVIOLENT") |
                    (df_incident_all["Incident_type"] == "Family offenses, no violence"), "Incident_category"] = "Domestic abuse incident"
  
# Driving related incident
                  
df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident")
                    & (df_incident_all["Incident_category"] != "Damage related incident") 
                    & (df_incident_all["Incident_category"] != "Domestic abuse incident") &
                    (df_incident_all["Incident_type"] == "TRAFFIC VIOLATION - HAZARDOUS") |
                    (df_incident_all["Incident_type"] == "UUMV") |
                    (df_incident_all["Incident_type"] == "TRAFFIC VIOLATION - NON HAZARDOUS"), "Incident_category"] = "Driving related incident"


# Drug related incident
df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident")
                    & (df_incident_all["Incident_category"] != "Damage related incident") 
                    & (df_incident_all["Incident_category"] != "Domestic abuse incident") 
                    & (df_incident_all["Incident_category"] != "Driving related incident") &
                    (df_incident_all["Incident_type"] == "NARCOTICS") |
                    (df_incident_all["Incident_type"] == "Drug equipment violations") |
                    (df_incident_all["Incident_type"] == "Narcotic / Drug Law Violations") |
                    (df_incident_all["Incident_type"] == "DRUG/ NARCOTIC VIOLATIONS") |
                    (df_incident_all["Incident_type"] == "DRUG EQUIPMENT VIOLATIONS") |
                    (df_incident_all["Incident_type"] == "Drug, narcotic violations") |
                    (df_incident_all["Incident_type"] == "drugs"), "Incident_category"] = "Drug related incident"

# fraud
df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident")
                    & (df_incident_all["Incident_category"] != "Damage related incident") & (df_incident_all["Incident_category"] != "Domestic abuse incident")
                    & (df_incident_all["Incident_category"] != "Driving related incident") &(df_incident_all["Incident_category"] != "Drug related incident") &
                    (df_incident_all["Incident_type"] == "DECEPTIVE PRACTICE") |
                    (df_incident_all["Incident_type"] == "Embezzlement") |
                    (df_incident_all["Incident_type"] == "Forgery and Counterfeiting") |
                    (df_incident_all["Incident_type"] == "Fraud") |
                    (df_incident_all["Incident_type"] == "Impersonation") |
                    (df_incident_all["Incident_type"] == "Gambling Violations") |
                    (df_incident_all["Incident_type"] == "EMBEZZELMENT") |
                    (df_incident_all["Incident_type"] == "CREDIT CARD/ ATM FRAUD") |
                    (df_incident_all["Incident_type"] == "IMPERSONATION") |
                    (df_incident_all["Incident_type"] == "FALSE PRETENSES/ SWINDLE/ CONFIDENCE GAME") |
                    (df_incident_all["Incident_type"] == "COUNTERFEITING / FORGERY") |
                    (df_incident_all["Incident_type"] == "BETTING/ WAGERING") |
                    (df_incident_all["Incident_type"] == "Welfare fraud") |
                    (df_incident_all["Incident_type"] == "Wire fraud") |
                    (df_incident_all["Incident_type"] == "Gambling equipment violations") |
                    (df_incident_all["Incident_type"] == "Bad checks") |
                    (df_incident_all["Incident_type"] == "Bribery") |
                    (df_incident_all["Incident_type"] == "Counterfeiting, forgery") |
                    (df_incident_all["Incident_type"] == "Credit card, ATM fraud") |
                    (df_incident_all["Incident_type"] == "Hacking/Computer Invasion") |
                    (df_incident_all["Incident_type"] == "False pretenses, swindle") |
                    (df_incident_all["Incident_type"] == "Extortion, Blackmail") |
                    (df_incident_all["Incident_type"] == "Promoting gambling") |
                    (df_incident_all["Incident_type"] == "Betting/wagering"), "Incident_category"] = "Fraud"
 
# human traffecking
df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident")
                    & (df_incident_all["Incident_category"] != "Damage related incident") & (df_incident_all["Incident_category"] != "Domestic abuse incident")
                    & (df_incident_all["Incident_category"] != "Driving related incident") &(df_incident_all["Incident_category"] != "Drug related incident") 
                    & (df_incident_all["Incident_category"] != "Fraud") &
                    (df_incident_all["Incident_type"] == "HUMAN TRAFFICKING") |
                    (df_incident_all["Incident_type"] == "Human Trafficking/Involuntary Servitude"), "Incident_category"] = "Sex offense related incident"
                    
# Murder incident
df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident")
                    & (df_incident_all["Incident_category"] != "Damage related incident") & (df_incident_all["Incident_category"] != "Domestic abuse incident")
                    & (df_incident_all["Incident_category"] != "Driving related incident") &(df_incident_all["Incident_category"] != "Drug related incident") 
                    & (df_incident_all["Incident_category"] != "Human Trafficking") &
                    (df_incident_all["Incident_type"] == "HOMICIDE") |
                    (df_incident_all["Incident_type"] == "Homicide - Criminal ") |
                    (df_incident_all["Incident_type"] == "Homicide - Criminal") |
                    (df_incident_all["Incident_type"] == "Homicide - Gross Negligence") |
                    (df_incident_all["Incident_type"] == "Homicide - Justifiable ") |
                    (df_incident_all["Incident_type"] == "MURDER & NONNEGLIGENT MANSLAUGHTER") |
                    (df_incident_all["Incident_type"] == "Murder") |
                    (df_incident_all["Incident_type"] == "Murder, non-negligent") |
                    (df_incident_all["Incident_type"] == "Negligent manslaughter"), "Incident_category"] = "Murder incident"

# sex incident
df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident")
                    & (df_incident_all["Incident_category"] != "Damage related incident") & (df_incident_all["Incident_category"] != "Domestic abuse incident")
                    & (df_incident_all["Incident_category"] != "Driving related incident") &(df_incident_all["Incident_category"] != "Drug related incident") 
                    & (df_incident_all["Incident_category"] != "Human Trafficking") & (df_incident_all["Incident_category"] != "Murder incident") &
                    (df_incident_all["Incident_type"] == "SEX OFFENSE") |
                    (df_incident_all["Incident_type"] == "PROSTITUTION") |
                    (df_incident_all["Incident_type"] == "CRIM SEXUAL ASSAULT") |
                    (df_incident_all["Incident_type"] == "CRIMINAL SEXUAL ASSAULT") |
                    (df_incident_all["Incident_type"] == "Prostitution and Commercialized Vice") |
                    (df_incident_all["Incident_type"] == "Other Sex Offenses (Not Commercialized)") |
                    (df_incident_all["Incident_type"] == "Rape") |
                    (df_incident_all["Incident_type"] == "Prostitution") |
                    (df_incident_all["Incident_type"] == "PORNOGRAPHY/ OBSCENE MATERIAL") |
                    (df_incident_all["Incident_type"] == "Pornographs, obscene material") |
                    (df_incident_all["Incident_type"] == "Purchasing prostitution") |
                    (df_incident_all["Incident_type"] == "Sexual assault with an object") |
                    (df_incident_all["Incident_type"] == "Statutory rape") |
                    (df_incident_all["Incident_type"] == "Human Trafficking/Commercial Sex Act") |
                    (df_incident_all["Incident_type"] == "Assisting or promoting prostitution") |
                    (df_incident_all["Incident_type"] == "Forcible sodomy") |
                    (df_incident_all["Incident_type"] == "Forcible rape") |
                    (df_incident_all["Incident_type"] == "Forcible fondling") |
                    (df_incident_all["Incident_type"] == "Incest") |
                    (df_incident_all["Incident_type"] == "SEX ABUSE"), "Incident_category"] = "Sex offense related incident"


# Robbery anf theft incident
df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident")
                    & (df_incident_all["Incident_category"] != "Damage related incident") & (df_incident_all["Incident_category"] != "Domestic abuse incident")
                    & (df_incident_all["Incident_category"] != "Driving related incident") &(df_incident_all["Incident_category"] != "Drug related incident") 
                    & (df_incident_all["Incident_category"] != "Human Trafficking") & (df_incident_all["Incident_category"] != "Murder incident") 
                    & (df_incident_all["Incident_category"] != "Sex offense related incident") &
                    (df_incident_all["Incident_type"] == "THEFT") |
                    (df_incident_all["Incident_type"] == "ROBBERY") |
                    (df_incident_all["Incident_type"] == "MOTOR VEHICLE THEFT") |
                    (df_incident_all["Incident_type"] == "BURGLARY") |
                    (df_incident_all["Incident_type"] == "BATTERY") |
                    (df_incident_all["Incident_type"] == "Thefts") |
                    (df_incident_all["Incident_type"] == "Theft from Vehicle") |
                    (df_incident_all["Incident_type"] == "Robbery No Firearm") |
                    (df_incident_all["Incident_type"] == "Robbery Firearm") |
                    (df_incident_all["Incident_type"] == "Receiving Stolen Property") |
                    (df_incident_all["Incident_type"] == "Burglary Non-Residential") |
                    (df_incident_all["Incident_type"] == "Burglary Residential") |
                    (df_incident_all["Incident_type"] == "Recovered Stolen Motor Vehicle") |
                    (df_incident_all["Incident_type"] == "BURGLARY-RESIDENCE") |
                    (df_incident_all["Incident_type"] == "THEFT FROM MOTOR VEHICLE") |
                    (df_incident_all["Incident_type"] == "ALL OTHER LARCENY") |
                    (df_incident_all["Incident_type"] == "SHOPLIFTING") |
                    (df_incident_all["Incident_type"] == "SHOPLIFTING") |
                    (df_incident_all["Incident_type"] == "ROBBERY-INDIVIDUAL") |
                    (df_incident_all["Incident_type"] == "BURGLARY-BUSINESS") |
                    (df_incident_all["Incident_type"] == "ROBBERY-BUSINESS") |
                    (df_incident_all["Incident_type"] == "ASSAULT") |
                    (df_incident_all["Incident_type"] == "POCKET-PICKING") |
                    (df_incident_all["Incident_type"] == "IDENTITY THEFT") |
                    (df_incident_all["Incident_type"] == "STOLEN PROPERTY OFFENSES") |
                    (df_incident_all["Incident_type"] == "THEFT OF BUILDING") |
                    (df_incident_all["Incident_type"] == "AutoTheft") |
                    (df_incident_all["Incident_type"] == "Purse-snatching") |
                    (df_incident_all["Incident_type"] == "Theft of motor vehicle parts or accessory") |
                    (df_incident_all["Incident_type"] == "Theft from building") |
                    (df_incident_all["Incident_type"] == "Identify theft") |
                    (df_incident_all["Incident_type"] == "Burglary, Breaking and Entering") |
                    (df_incident_all["Incident_type"] == "From coin-operated machine or device") |
                    (df_incident_all["Incident_type"] == "THEFT F/AUTO") |
                    (df_incident_all["Incident_type"] == "THEFT/OTHER") |
                    (df_incident_all["Incident_type"] == "bicycle-theft") |
                    (df_incident_all["Incident_type"] == "other-theft") |
                    (df_incident_all["Incident_type"] == "theft-from-the-person") |
                    (df_incident_all["Incident_type"] == "vehicle-crime") |
                    (df_incident_all["Incident_type"] == "All other larceny") |
                    (df_incident_all["Incident_type"] == "Arson") |
                    (df_incident_all["Incident_type"] == "Burglary") |
                    (df_incident_all["Incident_type"] == "THEFT OF MOTOR VEHICLE PARTS OR ACCESSORIES") |
                    (df_incident_all["Incident_type"] == "Robbery") |
                    (df_incident_all["Incident_type"] == "Theft") |
                    (df_incident_all["Incident_type"] == "Pocket-picking") |
                    (df_incident_all["Incident_type"] == "Shoplifting") |
                    (df_incident_all["Incident_type"] == "Stolen property offenses") |
                    (df_incident_all["Incident_type"] == "Theft from motor vehicle") |
                    (df_incident_all["Incident_type"] == "Motor Vehicle Theft") |
                    (df_incident_all["Incident_type"] == "Motor vehicle theft") |
                    (df_incident_all["Incident_type"] == "burglary") |
                    (df_incident_all["Incident_type"] == "robbery") |
                    (df_incident_all["Incident_type"] == "shoplifting") |
                    
                    (df_incident_all["Incident_type"] == "Break-ins"), "Incident_category"] = "Robbery and theft incident" 

                    
# Weapons related incident

df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident")
                    & (df_incident_all["Incident_category"] != "Damage related incident") & (df_incident_all["Incident_category"] != "Domestic abuse incident")
                    & (df_incident_all["Incident_category"] != "Driving related incident") &(df_incident_all["Incident_category"] != "Drug related incident") 
                    & (df_incident_all["Incident_category"] != "Human Trafficking") & (df_incident_all["Incident_category"] != "Murder incident") 
                    & (df_incident_all["Incident_category"] != "Sex offense related incident") & (df_incident_all["Incident_category"] != "Robbery and theft incident") &
                    (df_incident_all["Incident_type"] == "WEAPONS VIOLATION") |
                    (df_incident_all["Incident_type"] == "Weapon law violations") |
                    (df_incident_all["Incident_type"] == "Weapon Violations") |
                    (df_incident_all["Incident_type"] == "WEAPON LAW VIOLATIONS") |
                    (df_incident_all["Incident_type"] == "possession-of-weapons"), "Incident_category"] = "Weapons related incident"

# other incident

df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident")
                    & (df_incident_all["Incident_category"] != "Damage related incident") & (df_incident_all["Incident_category"] != "Domestic abuse incident")
                    & (df_incident_all["Incident_category"] != "Driving related incident") &(df_incident_all["Incident_category"] != "Drug related incident") 
                    & (df_incident_all["Incident_category"] != "Human Trafficking") & (df_incident_all["Incident_category"] != "Murder incident") 
                    & (df_incident_all["Incident_category"] != "Sex offense related incident") & (df_incident_all["Incident_category"] != "Robbery and theft incident") &
                    (df_incident_all["Incident_category"] != "Weapons related incident") &
                    (df_incident_all["Incident_type"] == "STALKING") |
                    (df_incident_all["Incident_type"] == "OBSCENITY") |
                    (df_incident_all["Incident_type"] == "OTHER OFFENSE") |
                    (df_incident_all["Incident_type"] == "All other offenses") |
                    (df_incident_all["Incident_type"] == "Animal Cruelty") |
                    (df_incident_all["Incident_type"] == "INTERFERENCE WITH PUBLIC OFFICER") |
                    (df_incident_all["Incident_type"] == "All Other Offenses") |
                    (df_incident_all["Incident_type"] == "ALL OTHER OFFENSES") |
                    (df_incident_all["Incident_type"] == "Vagrancy/Loitering") |
                    (df_incident_all["Incident_type"] == "MISCELLANEOUS") |
                    (df_incident_all["Incident_type"] == "Peeping tom") |
                    (df_incident_all["Incident_type"] == "Runaway") |
                    (df_incident_all["Incident_type"] == "Trespass of real property") |
                    (df_incident_all["Incident_type"] == "Curfew, loitering, vagrancy violations") |
                    (df_incident_all["Incident_type"] == "anti-social-behaviour") |
                    (df_incident_all["Incident_type"] == "other-crime") |
                    (df_incident_all["Incident_type"] == "public-order"), "Incident_category"] = "Other Incident"


# nuiance incidents
df_incident_all.loc[(df_incident_all["Incident_category"] != "Alcohol Related Incident") & (df_incident_all["Incident_category"] != "Assault related incident")
                    & (df_incident_all["Incident_category"] != "Damage related incident") & (df_incident_all["Incident_category"] != "Domestic abuse incident")
                    & (df_incident_all["Incident_category"] != "Driving related incident") &(df_incident_all["Incident_category"] != "Drug related incident") 
                    & (df_incident_all["Incident_category"] != "Human Trafficking") & (df_incident_all["Incident_category"] != "Murder incident") 
                    & (df_incident_all["Incident_category"] != "Sex offense related incident") & (df_incident_all["Incident_category"] != "Robbery and theft incident") &
                    (df_incident_all["Incident_category"] != "Other Incident") & 
                    (df_incident_all["Incident_type"] == "Registered Nuiance"), "Incident_category"] = "Nuisance Incident"

                    


df_incident_all.loc[(df_incident_all["Place"].str.contains("NETHERLANDS") == 1) , "Country"] = "Netherlands"

df_incident_all.loc[(df_incident_all["Place"].str.contains("USA") == 1) & 
                    (df_incident_all["Country"] != "Netherlands")  , "Country"] = "US"

df_incident_all.loc[(df_incident_all["Place"].str.contains("UK") == 1) & 
                    (df_incident_all["Country"] != "Netherlands") & 
                    (df_incident_all["Country"] != "United States") , "Country"] = "United Kingdom"




df_incident_all["Year"] = df_incident_all["Date"].str[:4]
df_incident_all["Year"] = df_incident_all["Year"].astype(int)


df_incident_2018 = df_incident_all[df_incident_all["Year"] == 2018]
df_incident_2019 = df_incident_all[df_incident_all["Year"] == 2019]
df_incident_2020 = df_incident_all[df_incident_all["Year"] == 2020]

df_temp = [df_incident_2018, df_incident_2019, df_incident_2020]
df_incident_all = pd.concat(df_temp)

del df_temp, df_incident_2018, df_incident_2019, df_incident_2020
        
df_incident_all = df_incident_all.groupby(["Date", "Country", "Incident_category"])["Incident_count"].sum().reset_index()

df_incident_all["Incident Category"] = df_incident_all["Incident_category"]

df_incident_all["Year"] = df_incident_all["Date"].str[:4]
df_incident_all["Year"] = df_incident_all["Year"].astype(int)



## SAFETY INDEX DATA ##
print("Processing Safety Index Data..")

# loading data into df
df_sid = pd.read_json("Safety_index_data.json")

# creating a seperate column for safety index
df_sid["Data"] = df_sid["Data"].str.strip()

# getting Safety index value from column Data
df_sid["Safety_index"] = df_sid["Data"].str[-7:]

# get rid of the number in Data column
df_sid["Data"] = df_sid["Data"].str[:-7]

# removing - from Safety_index column
df_sid["Safety_index"] = df_sid["Safety_index"].str.replace("-","")

# convert Safety_index to float
df_sid["Safety_index"] = pd.to_numeric(df_sid["Safety_index"], errors="coerce")

# creating a new df without the value "Rank - City - Safety Index"
df_sid = df_sid[df_sid["Data"] != "Rank - City - Safety Index"]


# df_sid["Pos"] = df_sid["Data"].str.find("-")
df_sid["Country"] = df_sid["Data"].str.split(",").str[1]
df_sid["City"] = df_sid["Data"].str.split(",").str[0]
df_sid["Country"] = df_sid["Country"].str.strip()


df_sid.loc[df_sid["Data"].str.contains("United States") == 1, "Country"] = "US"

df_sid = df_sid[df_sid["City"] != "Rochester"]
df_sid = df_sid[df_sid["City"] !=  "Richmond"]
df_sid = df_sid[df_sid["City"] != "Jacksonville"]
df_sid = df_sid[df_sid["City"] != "Indianapolis"]
df_sid = df_sid[df_sid["City"] != "Tucson"]
df_sid = df_sid[df_sid["City"] != "Madison"]
df_sid = df_sid[df_sid["City"] != "Irvine"]
df_sid = df_sid[df_sid["City"] != "Memphis"]
df_sid = df_sid[df_sid["City"] != "Cleveland"]
df_sid = df_sid[df_sid["City"] != "Anchorage"]
df_sid = df_sid[df_sid["City"] != "Spokane"]
df_sid = df_sid[df_sid["City"] != "Louisville"]
df_sid = df_sid[df_sid["City"] != "Omaha"]
df_sid = df_sid[df_sid["City"] != "Raleigh"]
df_sid = df_sid[df_sid["City"] != "El Paso"]
df_sid = df_sid[df_sid["City"] != "Cardiff"]
df_sid = df_sid[df_sid["City"] != "Sheffield"]
df_sid = df_sid[df_sid["City"] != "Bradford"]
df_sid = df_sid[df_sid["City"] != "Bristol"]
df_sid = df_sid[df_sid["City"] != "Brighton"]
df_sid = df_sid[df_sid["City"] != "Aberdeen"]
df_sid = df_sid[df_sid["City"] != "Utrecht"]
df_sid = df_sid[df_sid["City"] != "Groningen"]

# df_sid.to_csv("test.csv")
# mylist = df_incident_all["Incident Category"].unique()
# print(mylist)
# mydict = {"hi" : mylist}
# print(mydict)

# for key, items in mydict.items():
#     print(items)

####COUNTRY DISPLAY OPTIONS####
df_usa_display = df_incident_all[df_incident_all["Country"] == "US"]
df_nl_display = df_incident_all[df_incident_all["Country"] == "Netherlands"]
df_uk_display = df_incident_all[df_incident_all["Country"] == "United Kingdom"]
us_display_list = df_usa_display["Incident Category"].unique()
us_display_list = np.append(us_display_list,"All")
nl_display_list = df_nl_display["Incident Category"].unique()
nl_display_list = np.append(nl_display_list,"All")
uk_display_list = df_uk_display["Incident Category"].unique()
uk_display_list = np.append(uk_display_list,"All")



country_display_options = {"US" : us_display_list,"United Kingdom" : uk_display_list,"Netherlands" : nl_display_list}

del df_usa_display, df_uk_display, df_nl_display, us_display_list, uk_display_list, nl_display_list
####CITY DISPLAY OPTIONS####
df_city_usa = df_sid[df_sid["Country"] == "US"]
df_city_uk = df_sid[df_sid["Country"] == "United Kingdom"]
df_city_nl = df_sid[df_sid["Country"] == "Netherlands"]

us_city_display_list = df_city_usa["City"].unique()
us_city_display_list = np.append(us_city_display_list, "All")
uk_city_display_list = df_city_uk["City"].unique()
uk_city_display_list = np.append(uk_city_display_list, "All")
nl_city_display_list = df_city_nl["City"].unique()
nl_city_display_list = np.append(nl_city_display_list, "All")

city_display_list = {"US" : us_city_display_list, "United Kingdom" : uk_city_display_list, "Netherlands" : nl_city_display_list}
del df_city_usa, df_city_uk, df_city_nl, us_city_display_list, uk_city_display_list, nl_city_display_list



# ##############################################
# #                                            #
# ############# DASH VISUALIZATION #############
# #                                            #
# ##############################################


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


fig_covid19 = px.line(df_covid19, x= "date", y = "Cases", line_group="Country",
                      hover_name = "Country", color = "Country")
fig_crime = px.line(df_incident_all, x = "Date", y = "Incident_count", line_group="Incident_category")



app.layout = html.Div(
    
    
    style = {"backgroundColor" : "#111111"},
    children=[
    
    html.H1(
        children='Crime and Incident Rates During the Pandamic',
            style = {
                "textAlign" : "center",
                "color" : "#ffffff"
                }
            ),

    html.Div(
    style={
        "textAlign" : "left"
        }
    ),
    
    html.Label("Please pick a country", style = {"color" : "#ffffff"}),
    dcc.Dropdown(
        id = "countries-dropdown",
        options = [
            {"label": "United States" , "value" : "US"},
            {"label": "United Kingdom" , "value" : "United Kingdom"},
            {"label": "Netherlands" , "value" : "Netherlands"}
            ],
        value = "US",
        style = {"width" : "50%","display" : "inline-block" },
        clearable = False,
        # placeholder = "Select a country",
        searchable = False,
        
        ),
    dcc.Dropdown(
        id = "incident-selection-dropdown",
        style = {"width" : "50%","display" : "inline-block" },
        options = [],
        value = "All",
        clearable = False,
        searchable = False
        
        ),
    html.Div(children = [
        
        html.Div(id = "us-selection-message",children = [], style = {"textAlign" : "Right", "color" : "#b8b20d"}),
        
        dcc.Graph(
            id = "corona-graph-output",
            figure ={},
            style = {"display" : "inline-block",
                     "margin-left" : "1%"}
        ),
        
        
        dcc.Graph(
            id = "incident-graph-output",
            figure ={},
            style = {"display" : "inline-block"},
            ),
        ],
    ),
    
      html.Br(),
      
    html.Div(children = [
        html.Div( children = [
            html.Label("Please pick a city", style = {"color" : "#ffffff",  "margin-left" : "51%"}),
            dcc.Dropdown(
            id = "city-selection-dropdown",
            style = {"width" : "50%","display" : "inline-block",
                      "margin-left" : "34%"},
            options = [],
            searchable = False,
            clearable = False,
            value = "All"
            
            ),
        
        html.Label("Please pick a Year", style = {"color" : "#ffffff"}),
        dcc.RadioItems(
            id = "year-selection-radioitem",
            options = [
                {"label" : "2018" , "value":2018},
                {"label" : "2019", "value": 2019},
                {"label" : "2020", "value": 2020},
                ],
                value = 2018,
                labelStyle={'display': 'inline-block', "color": "#ffffff"},
                
            )

        ]),

        
        html.Br(),
        dcc.Graph(
            id = "crime-pie-chart",
            figure ={},
            style = {"display" : "inline-block",
                     "margin-left" : "1%"}
            ),
        dcc.Graph(
            id = "safety-index-chart",
            figure = {},
            style = {"display" : "inline-block"}
            )
        
        ])

    
])


@app.callback(
    Output(component_id='corona-graph-output', component_property='figure'),
    Output(component_id='incident-selection-dropdown', component_property='value'),
    Output(component_id='city-selection-dropdown', component_property='value'),
    [Input(component_id='countries-dropdown', component_property='value')]
)
def update_covid_chart(selected_country):
    filtered_df = df_covid19[df_covid19["Country"] == selected_country]    
    fig_covid = px.bar(filtered_df, x = "date", y = "Cases" , 
                  hover_name= "Cases", color = "Cases", title="Covid 19 Cases",
                  hover_data={"Cases", "date"})
    fig_covid.update_layout(
        plot_bgcolor = "#111111",
        paper_bgcolor = "#111111",
        font_color = "#2591cc"
        )
    return fig_covid, "All", "All"

@app.callback(
    Output(component_id='incident-graph-output', component_property='figure'),
    Output(component_id='us-selection-message', component_property='children'),
    [Input(component_id='countries-dropdown', component_property='value')],
     [Input(component_id='incident-selection-dropdown', component_property='value')]
)
def update_incident_chart(selected_country, selected_incident):
    container = ""
    if selected_country == "US":
        container = "Crime and Incident Data collected is based on USA Cities: Chicago, Dallas, Philadelphia, San Francisco, DC and Houston"
    else:
        container = ""
    
    if selected_incident == "All":
        filtered_incident_df = df_incident_all[df_incident_all["Country"] == selected_country]
        fig_incident = px.line(filtered_incident_df, x = "Date", y = "Incident_count",
                               line_group = "Incident Category" ,color = "Incident Category",
                               title = "Incidents and Crime Graph",hover_name = "Incident Category")
    else:
        filtered_incident_df = df_incident_all[df_incident_all["Country"] == selected_country]
        filtered_incident_df = filtered_incident_df[filtered_incident_df["Incident Category"] == selected_incident]
        fig_incident = px.line(filtered_incident_df, x = "Date", y = "Incident_count",
                               line_group = "Incident Category" ,color = "Incident Category",
                               title = "Incidents and Crime Graph",hover_name = "Incident Category")
    fig_incident.update_layout(
        plot_bgcolor = "#111111",
        paper_bgcolor = "#111111",
        font_color = "#2591cc"
        )
    return fig_incident, container

@app.callback(
    Output(component_id='crime-pie-chart', component_property='figure'),
    [Input(component_id='countries-dropdown', component_property='value')],
    [Input(component_id='year-selection-radioitem', component_property='value')]
)

def update_pie_chart(selected_country, selected_year):
    
    filtered_incident_year_df = df_incident_all[df_incident_all["Country"] == selected_country]
    filtered_incident_year_df = filtered_incident_year_df[filtered_incident_year_df ["Year"] == selected_year]
    
    fig_inc_pie = px.pie(filtered_incident_year_df, values = "Incident_count", names = "Incident Category",
                          title = "Incident Distribution")
    fig_inc_pie.update_layout(
        plot_bgcolor = "#111111",
        paper_bgcolor = "#111111",
        font_color = "#2591cc"
        )
    
    return fig_inc_pie

@app.callback(
    Output(component_id='safety-index-chart', component_property='figure'),
    [Input(component_id='countries-dropdown', component_property='value')],
    [Input(component_id='year-selection-radioitem', component_property='value')],
    [Input(component_id='city-selection-dropdown', component_property='value')]
)

def update_si_chart(selected_country, selected_year, selected_city):
    if selected_city == "All":
        df_filtered_sid = df_sid[df_sid["Country"] == selected_country]
        df_filtered_sid["Year"] = df_filtered_sid["Year"].astype(int)
        df_filtered_sid = df_filtered_sid.sort_values(by = "City")
        df_filtered_sid = df_filtered_sid[df_filtered_sid["Year"] == selected_year]
        fig_sid = px.bar(df_filtered_sid, x = "Safety_index", y = "City",
                                   color = "City", title = "Cities Safety Index", hover_name = "City", hover_data={"Safety_index"})
    else:
        df_filtered_sid = df_sid[df_sid["Country"] == selected_country]
        df_filtered_sid["Year"] = df_filtered_sid["Year"].astype(int)
        df_filtered_sid = df_filtered_sid.sort_values(by = "City")
        df_filtered_sid = df_filtered_sid[df_filtered_sid["Year"] == selected_year]
        df_filtered_sid = df_sid[df_sid["City"] == selected_city]
        fig_sid = px.bar(df_filtered_sid, x = "Safety_index", y = "City",
                                   color = "City", title = "Cities Safety Index",hover_name = "City", hover_data={"Safety_index"})
       
    
    fig_sid.update_layout(
    plot_bgcolor = "#111111",
    paper_bgcolor = "#111111",
    font_color = "#2591cc"
    )
    
  
    
    return fig_sid

@app.callback(
    Output(component_id='incident-selection-dropdown', component_property='options'),
    [Input(component_id='countries-dropdown', component_property='value')]
    
 )
def update_incident_dropdown(selected_country):
    
    return [{"label" : i , "value" : i} for i in country_display_options[selected_country]]
    


@app.callback(
    Output(component_id='city-selection-dropdown', component_property='options'),
    [Input(component_id='countries-dropdown', component_property='value')]   
)
def update_cityselection_dropdown(selected_country):
    return[{"label" : i, "value" : i} for i in city_display_list[selected_country]]


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
        


    


    