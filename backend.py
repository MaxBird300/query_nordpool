# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:52:27 2021

Documentation for API can be found here - https://marketdata.nordpoolgroup.com/docs/services/MarketData-UK-v2/operations/UkAreaPrices?


@author: maxbi
"""
import requests
import datetime
import sys
import pandas as pd

def strDate2iso(strDate):
    dt = datetime.datetime.strptime(strDate, "%d/%m/%Y")
    return dt.isoformat() + "Z"


class NordPoolClass:
    
    def __init__(self, username: str, password: str, sub_key: str):
        self.username = username
        self.password = password
        self.mySession = requests.Session()
        self.subKey = sub_key
        
    def authenticateUser(self):
        """
        Returns authentication token as explained in - https://developers.nordpoolgroup.com/docs/auth-introduction
    
        """
        marketDataAuth = "Y2xpZW50X21hcmtldGRhdGFfYXBpOmNsaWVudF9tYXJrZXRkYXRhX2FwaQ==" # these are defined here: https://developers.nordpoolgroup.com/v1.0/docs/clients-and-scopes
        
        headers = {"Authorization": "Basic " + marketDataAuth,
                   "Content-Type": "application/x-www-form-urlencoded"}
        
        payload = {"grant_type": "password",
                   "scope": "marketdata_api",
                   "username": self.username,
                   "password": self.password}
        try:
            response = self.mySession.post("https://sts.nordpoolgroup.com/connect/token", data = payload, headers = headers)
            if response.status_code == 200:
                print("Authentication success! Token received.")
                self.token = response.json()['access_token'] 
            else:
                print("Authentication failed, status code: %s" % response.status_code)
                sys.exit(0)
        except requests.exceptions.RequestException as err:
            print(err)
            sys.exit(0)


    def apiResponse(self, host, payload, headers):

        try:
            response = self.mySession.get(host, params = payload, headers = headers) 
            if response.status_code == 200:
                print('Request successful! Data received.')
                return response
            else:
                print('Request failed, status code: %s' % response.status_code)
                sys.exit(0)
        except requests.exceptions.RequestException as err:
            print(err)
            sys.exit(0)
            
    
    def dayAheadData(self, startDate, endDate):
        
        # Authenticate and assign token
        self.authenticateUser()
        
        # change string dates to ISO datetime
        startTime = strDate2iso(startDate)
        endTime = strDate2iso(endDate)
        
        # change the below 'host' 'payload' and 'headers' to access different parts of the API found here - https://marketdata.nordpoolgroup.com/docs/services/MarketData-UK-v2/operations/UkAreaBlockPrices 
        host = "https://marketdata-api.nordpoolgroup.com/uk/v2/n2ex/prices/area?" 
        payload = {"startTime": startTime,
                   "endTime": endTime}
        headers = {"Accept-Encoding": '',
                    "Ocp-Apim-Subscription-Key": self.subKey,
                    "Authorization": "Bearer " + self.token}
        
        # get response object from API
        response = self.apiResponse(host, payload, headers)
        hourly_prices = response.json()[0]['values'] # dictionary of hourly prices
        
        df = pd.DataFrame(
            data = {
                'Timestamp': [x['startTime'] for x in hourly_prices],
                'Price (GBP/MWh)': [x['value'] for x in hourly_prices]          
                }
            )
        
        return df

        