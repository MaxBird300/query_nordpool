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
        
        self.set_new_authentication_token()   
        
    def set_new_authentication_token(self):
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
                self.token_expiration = (
                    datetime.datetime.now() 
                    + datetime.timedelta(seconds=response.json()['expires_in'])
                    )

            else:
                print("Authentication failed, status code: %s" % response.status_code)

        except requests.exceptions.RequestException as err:
            print(err)

    
    def check_authentication_token(self):
        if datetime.datetime.now() > self.token_expiration:
            self.set_new_authentication_token()

    def apiResponse(self, host, payload, headers):

        try:
            response = self.mySession.get(host, params = payload, headers = headers) 
            if response.status_code == 200:
                # print('Request successful! Data received.')
                return response
            else:
                print('Request failed, status code: %s' % response.status_code)
                sys.exit(0)
        except requests.exceptions.RequestException as err:
            print(err)
            sys.exit(0)
    
    
    def UKdayAheadPricesV2(
            self,
            delivery_date: str # delivery CET date, yyyy-MM-dd format e.g. 2024-01-21
            ):
        """
        Returns settled hourly day-ahead prices for UK for specified delivery_date.
        
        Prices are set 9am the day before delivery I think...
        """

        # Authenticate and assign token if required
        self.check_authentication_token()
        
        host = 'https://data-api.nordpoolgroup.com/api/v2/Auction/Prices/ByAreas?'
        payload = {
            'market': 'N2EX_DayAhead',
            'areas': 'UK',
            'currency': 'GBP',
            'date': delivery_date
            }
        headers = {
            "Accept-Encoding": '',
            "Ocp-Apim-Subscription-Key": self.subKey,
            "Authorization": "Bearer " + self.token
            }
        response = self.apiResponse(host, payload, headers)
        price_dicts = response.json()[0]['prices'] # list of dicts

        df = pd.DataFrame(
            data = {
                'Timestamp': [x['deliveryStart'] for x in price_dicts],
                'Price (GBP/MWh)': [x['price'] for x in price_dicts]          
                }
            )
        
        return df
    
    def get_day_ahead_prices(
            self,
            start_date: str, # YYYY-mm-dd format
            end_date: str, # YYYY-mm-dd format
            ):
        
        query_dates = pd.date_range(start_date, end_date, freq='D')
        delivery_dates = [x.strftime('%Y-%m-%d') for x in query_dates]
        
        results = []
        for delivery_date in delivery_dates:
            results.append(self.UKdayAheadPricesV2(delivery_date))
            
        return pd.concat(results, axis=0).reset_index(drop=True)
        
    
    def UkdayAheadPriceCurve(
            self,
            delivery_date: str # delivery CET date, yyyy-MM-dd format e.g. 2024-01-21
            ):
        
        self.check_authentication_token()
        
        host = 'https://data-api.nordpoolgroup.com/api/v2/Auction/N2EX_DayAhead/PriceCurves/UK?'
        payload = {
            'date': delivery_date
            }
        
        headers = {
            "Accept-Encoding": '',
            "Ocp-Apim-Subscription-Key": self.subKey,
            "Authorization": "Bearer " + self.token
            }
        
        response = self.apiResponse(host, payload, headers)
        
        order_positions = response.json()['orderPositions'] # list of 24 dicts for demand/supply curves for each hour
        
        
        return order_positions
        
        