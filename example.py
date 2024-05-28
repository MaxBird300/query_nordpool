# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:52:27 2021

Documentation for API can be found here - https://marketdata.nordpoolgroup.com/docs/services/MarketData-UK-v2/operations/UkAreaPrices?

@author: maxbi
"""
from backend import NordPoolClass
import config

delivery_date = '2012-01-01' # yyyy-MM-dd format


nordPoolAPI = NordPoolClass(config.username, config.password, config.sub_key) # initialise the API connection
df = nordPoolAPI.UKdayAheadPricesV2(delivery_date)

