# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:52:27 2021

Documentation for API can be found here - https://marketdata.nordpoolgroup.com/docs/services/MarketData-UK-v2/operations/UkAreaPrices?

@author: maxbi
"""
import pandas as pd
import matplotlib.pyplot as plt

from backend import NordPoolClass
import config


def extract_supply_demand_curves(order_positions: dict, hour_to_analyse):
    
    curve_data = order_positions[hour_to_analyse]
    
    demand_curve = pd.DataFrame(
        data = {
            'Price (GBP/MWh)': [x['price'] for x in curve_data['demandCurve']],
            'Volume (MWh)': [x['volume'] for x in curve_data['demandCurve']],
            }
        )
    
    supply_curve = pd.DataFrame(
        data = {
            'Price (GBP/MWh)': [x['price'] for x in curve_data['supplyCurve']],
            'Volume (MWh)': [x['volume'] for x in curve_data['supplyCurve']],
            }
        )
    
    return supply_curve, demand_curve

def plot_supply_demand_curves(order_positions, hour_to_plot, xlims: list=None, ylims: list=None):
    
    # extract plotting data
    supply_curve, demand_curve = extract_supply_demand_curves(order_positions, hour_to_plot)
    start_time = order_positions[hour_to_plot]['deliveryStart']
    end_time = order_positions[hour_to_plot]['deliveryEnd']

    
    # do plotting
    fig, axes = plt.subplots(1, figsize=(6,4), dpi=250)
    axes.set_title(f'Supply/Demand Curves for {start_time} - {end_time}')
    axes.plot(supply_curve['Volume (MWh)'], supply_curve['Price (GBP/MWh)'], label='supply_curve')
    axes.plot(demand_curve['Volume (MWh)'], demand_curve['Price (GBP/MWh)'], label='demand_curve')
    axes.set_xlabel('Volume [MWh]')
    axes.set_ylabel('Price [£/MWh]')
    axes.legend()
    axes.grid()
    axes.set_ylim(ylims)
    axes.set_xlim(xlims)

delivery_date = '2024-05-25' # yyyy-MM-dd format

nordPoolAPI = NordPoolClass(config.username, config.password, config.sub_key) # initialise the API connection
order_positions = nordPoolAPI.UkdayAheadPriceCurve(delivery_date) # list of dicts for supply/demand curves at each hour of the day
plot_supply_demand_curves(order_positions, hour_to_plot = 19)
plot_supply_demand_curves(order_positions, hour_to_plot = 19, xlims = [9000,12000], ylims=[0,400])























