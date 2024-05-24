# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:52:27 2021

Documentation for API can be found here - https://marketdata.nordpoolgroup.com/docs/services/MarketData-UK-v2/operations/UkAreaPrices?

@author: maxbi
"""
from backend import NordPoolClass
import config

startDate = '01/01/2020' # don't query more than one month at a time, dd/mm/yyyy format
endDate = '01/02/2020'

delivery_date = '2024-05-25' # yyyy-MM-dd format


nordPoolAPI = NordPoolClass(config.username, config.password, config.sub_key) # initialise the API connection
# df = nordPoolAPI.dayAheadData(startDate, endDate) # Timestamp in output dataframe relates to the start of the time period
df_v2 = nordPoolAPI.UKdayAheadPricesV2(delivery_date)
