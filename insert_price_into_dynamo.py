# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:31:59 2024

@author: Max
"""
import pandas as pd
from datetime import datetime
import time
import requests
import boto3
from decimal import Decimal, getcontext
getcontext().prec = 2

from backend import NordPoolClass
import config
import ddbwrapper as dbw

def timestamp2unix(str_timestamp: str) -> int:
    utc_dt = datetime.strptime(str_timestamp, '%Y-%m-%dT%H:%M:%SZ')
    unix_timestamp = (utc_dt - datetime(1970, 1, 1)).total_seconds()
    return int(unix_timestamp)

def format_dynamo_items(day_ahead_prices: pd.DataFrame) -> list[dict]:

    # extract data
    prices = [day_ahead_prices.to_dict()['Price (GBP/MWh)'][x] for x in range(len(day_ahead_prices))]
    timestamps = [day_ahead_prices.to_dict()['Timestamp'][x] for x in range(len(day_ahead_prices))]
    unix_timestamps = [timestamp2unix(x) for x in timestamps]
    
    items = []
    for unix_timestamp, str_timestamp, elec_price in zip(unix_timestamps, timestamps, prices):
    
        items.append({
            'PK': 'nordpool_elec_price',
            'unixTimestamp': unix_timestamp,
            # 'delivery_timestamp': str_timestamp,
            'elec_price_GBP/MWh': Decimal(str(elec_price))
            })
    
    return items


def write_nordpool_price_to_dynamo(
        start_date: str, # YYYY-mm-dd format
        end_date: str, # YYYY-mm-dd format
        table_name: str='bmsTrial'
        ):

    query_dates = pd.date_range(start_date, end_date, freq='D')
    delivery_dates = [x.strftime('%Y-%m-%d') for x in query_dates]
    nordPoolAPI = NordPoolClass(config.username, config.password, config.sub_key) # initialise the API connection
    dynamo_table = boto3.resource('dynamodb').Table(table_name)
    
    day_counter = 0
    for delivery_date in delivery_dates:
    
        day_ahead_prices = nordPoolAPI.UKdayAheadPricesV2(delivery_date)
        list_of_items = format_dynamo_items(day_ahead_prices)
        
        with dynamo_table.batch_writer() as batch:
            for item in list_of_items:
                batch.put_item(item)
        
        day_counter += 1
        if day_counter % 30 == 0:
            print(f'Completed up to: {delivery_date}')
        
            
            
start_date = '2024-01-01'
end_date = '2024-05-28'
 
write_nordpool_price_to_dynamo(start_date, end_date, table_name='bmsTrial')

    

# # test put worked as expected
# unix_start = dbw.timestamp2unix('00:00 01/01/2020')
# unix_end = 	dbw.timestamp2unix('00:00 01/02/2020')

# table_class = dbw.dynamoTable('bmsTrial')
# items, empty_response = table_class.queryDynamo('nordpool_elec_price', unix_start, unix_end)

# # extract data
# prices = [float(items[x]['elec_price_GBP/MWh']) for x in range(len(items))]
# unix_timestamps = [int(items[x]['unixTimestamp']) for x in range(len(items))]

# price_data_df = pd.Series(
#     data = prices,
#     index = pd.to_datetime(unix_timestamps, unit="s", origin="unix", utc=True).tz_convert("Europe/London"),
#     name = 'n2ex_elec_price_£/MWh'
#     )



