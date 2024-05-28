# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:52:27 2021

Documentation for API can be found here - https://marketdata.nordpoolgroup.com/docs/services/MarketData-UK-v2/operations/UkAreaPrices?

@author: maxbi
"""
from backend import NordPoolClass
import config

# initialise NordPoolAPI Class
nordPoolAPI = NordPoolClass(config.username, config.password, config.sub_key) # initialise the API connection

# query day ahead prices for one specific delivery date (e.g. 24 hours of data)
delivery_date = '2024-05-29' # yyyy-MM-dd format
df = nordPoolAPI.UKdayAheadPricesV2(delivery_date)

# query multiple days of day-ahead prices (wrapper of above function)
start_date = '2024-05-26'
end_date = '2024-05-29'
df2 = nordPoolAPI.get_day_ahead_prices(start_date, end_date)

