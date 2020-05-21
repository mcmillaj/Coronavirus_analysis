import pandas as pd
import numpy as np
import requests
from datetime import datetime
import os
import pathlib
import csv

def getBingData(force_refresh = False, save_data = 'Both'):

    today = datetime.date(datetime.now())
    file_name = pathlib.Path('Original_data/BING-COVID19-Data_' + str(today) + '.csv')
    if file_name.exists() and force_refresh != True:
        print('Loading previously saved data...')
        daily_data = pd.read_csv(file_name)
    else:
        print('Downloading data from github...')
        url = 'https://raw.githubusercontent.com/microsoft/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv'
        try:
            daily_data = pd.read_csv(url, parse_dates = [1])
        except:
            print('Error retrieving data from github')
            return None 
        daily_data.to_csv(file_name)
        #daily_data.to_csv(pathlib.Path('Working_data',file_name.stem + 'feather')
    return daily_data



# test data aggregation
df = getBingData()

df['Country_Region'].unique()



def totalRegion(df, metric, country = None, state = None):
    
    if metric not in ['Confirmed','Deaths']:
        print('Metric must be "Confirmed" or "Deaths"')
    if country != None:
        country_data = df[df.Country_Region == country]
        country_only = country_data[country_data.AdminRegion1.isnull()]
        country_total = country_only.sort_values('Updated').tail(1)[metric].sum()
        print(country_total)
        return country_total
    elif state != None:
        state_data = df[df.AdminRegion1 == state]
        state_only = state_data[state_data.AdminRegion2.isnull()]
        state_total = state_only.sort_values('Updated').tail(1)[metric].sum()
        print(state_total)
        return state_total
    else:
        world_only = df[df.Country_Region == 'Worldwide']
        world_total = world_only.sort_values('Updated').tail(1)[metric].sum()
        print(world_total)
        return world_total

def testAggregation(df, country = None, state = None):

    if country != None:
        country_data = df[df.Country_Region == country]
        country_only = country_data[country_data.AdminRegion1.isnull()]
        state_only = country_data[country_data.AdminRegion1.notnull() & country_data.AdminRegion2.isnull()]
        county_only = country_data[country_data.AdminRegion1.notnull() & country_data.AdminRegion2.notnull()]

        country_total = country_only.sort_values('Updated').tail(1).Confirmed.sum()
        state_agg = state_only.sort_values(['AdminRegion1','Updated']).groupby('AdminRegion1').tail(1).Confirmed.sum()
        county_agg = county_only.sort_values(['AdminRegion2','Updated']).groupby('AdminRegion2').tail(1).Confirmed.sum()
        print('State percentage is: ' + str(round(state_agg / country_total * 100, 1)) + '%')
        print('County percentage is: ' + str(round(county_agg / country_total * 100, 1)) + '%')
    elif state != None:
        state_data = df[df.AdminRegion1 == state]
        state_only = state_data[state_data.AdminRegion2.isnull()]
        county_only = state_data[state_data.AdminRegion2.notnull()]

        state_total = state_only.sort_values('Updated').tail(1).Confirmed.sum()
        county_agg = county_only.sort_values(['AdminRegion2','Updated']).groupby('AdminRegion2').tail(1).Confirmed.sum()
        print('County percentage is: ' + str(round(county_agg / state_total * 100, 1)) + '%')
    else:
        world_only = df[df.Country_Region == 'Worldwide']
        country_only = df[(df.Country_Region != 'Worldwide') & (df.AdminRegion1.isnull())]
        world_total = world_only.sort_values('Updated').tail(1).Confirmed.sum()
        country_agg = country_only.sort_values(['Country_Region','Updated']).groupby('Country_Region').tail(1).Confirmed.sum()
        print('Country percentage is: ' + str(round(country_agg / world_total * 100, 1)) + '%')

# Some data is lost when summing by more granular locations. 
testAggregation(df, country = 'United States')
testAggregation(df, state = 'Colorado')
testAggregation(df, country = 'China (mainland)')
testAggregation(df, country = 'United Kingdom')



# Make prediction models
# Make coefficient model
# Make python charts
# Make tableau charts
# Clean and document code
# Make jupyter notebook
# If time: make curve inflection analysis
# If time: make curve analysis charts