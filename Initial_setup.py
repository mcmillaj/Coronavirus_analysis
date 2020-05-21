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





