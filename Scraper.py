import pandas as pd
import pickle
import bs4 as bs
import os
from os.path import exists
import requests
import sys

from googlefinance.client import get_prices_time_data
import quandl
from alpha_vantage.timeseries import TimeSeries
from fredapi import Fred


"""
- Allow to scrape any source (fed rates, bonds, stocks, indices)
- Allow update feature (while maintaining directory)
- Allow for specifying directory
- Output pandas dataframe

STOCK:
    - Required: symbol, time period, interval (only for time-series-intraday)
    - Optional: datatype

    TIME PARAMETER OPTIONS

        - intraday: This API returns intraday time series (timestamp, open, high, low, close, volume)
        of the equity specified, updated realtime.

        - daily: This API returns daily time series (date, daily open, daily high, daily low, daily close,
        daily volume) of the equity specified, covering up to 20 years of historical data

        - daily_adjusted: This API returns daily time series (date, daily open, daily high, daily low,
        daily close, daily volume, daily adjusted close, and split/dividend events) of the equity
        specified, covering up to 20 years of historical data.

        - weekly: This API returns weekly time series (last trading day of each week, weekly open,
        weekly high, weekly low, weekly close, weekly volume) of the equity specified, covering up
        to 20 years of historical data.

        - weekly_adjusted: This API returns weekly adjusted time series (last trading day of each week,
        weekly open, weekly high, weekly low, weekly close, weekly adjusted close, weekly volume,
        weekly dividend) of the equity specified, covering up to 20 years of historical data.

        - monthly: This API returns monthly time series (last trading day of each month, monthly open,
        monthly high, monthly low, monthly close, monthly volume) of the equity specified,
        covering up to 20 years of historical data.

        - monthly_adjusted: This API returns monthly adjusted time series (last trading day of each
        month, monthly open, monthly high, monthly low, monthly close, monthly adjusted close,
        monthly volume, monthly dividend) of the equity specified, covering up to 20 years of
        historical data.

"""

def alpha_vantage_pull():
    key_and_instrument = input('api key and instrument: ')
    if key_and_instrument == '?':
        print_instructions()
    api_key = key_and_instrument.split(' ')[0]
    instrument = key_and_instrument.split(' ')[1]
    ts = TimeSeries(key=api_key, output_format='pandas')
    if instrument == 'stock':
        stock_scrape(ts, api_key, instrument)

def stock_scrape(ts, api_key, instrument):

    print("symbol, time period, data to keep"
          "\nexample: AAPL weekly_adjusted OCV")
    try:
        user_input = input('')
        if user_input == '?':
            print_instructions()
        stock = user_input.split(' ')[0]
        time_period = user_input.split(' ')[1]
        data_to_keep = user_input.split(' ')[2]

        if time_period == 'intraday':
            print("interval (default = '1min')")
            interval = input('')
            if interval == '?':
                print_instructions()
            interval = '1min' if interval == '' else interval

            ticker, meta_data = ts.get_intraday(symbol=stock, interval=interval)
            df = keep_data(ticker, data_to_keep)
            save_locally(df)

        elif time_period == 'daily':
            ticker, meta_data = ts.get_daily(symbol=stock)
            df = keep_data(ticker, data_to_keep)
            save_locally(df)

        elif time_period == 'daily_adjusted':
            ticker, meta_data = ts.get_daily_adjusted(symbol=stock)
            df = keep_data(ticker, data_to_keep)
            save_locally(df)

        elif time_period == 'weekly':
            ticker, meta_data = ts.get_weekly(symbol=stock)
            df = keep_data(ticker, data_to_keep)
            save_locally(df)

        elif time_period == 'weekly_adjusted':
            ticker, meta_data = ts.get_weekly_adjusted(symbol=stock)
            df = keep_data(ticker, data_to_keep)
            save_locally(df)

        elif time_period == 'monthly':
            ticker, meta_data = ts.get_monthly(symbol=stock)
            df = keep_data(ticker, data_to_keep)
            save_locally(df)

        elif time_period == 'monthly_adjusted':
            ticker, meta_data = ts.get_monthly_adjusted(symbol=stock)
            df = keep_data(ticker, data_to_keep)
            save_locally(df)

    except IndexError:
        print("Incorrect Input. Enter '?' for instructions. Press Enter to launch scraper again")
        error_input = input('')
        print_instructions() if error_input == '?' else stock_scrape(ts, api_key, instrument)

def keep_data(dataframe, data_to_keep):
    if data_to_keep == '':
        return dataframe
    else:
        data = [i.lower() for i in list(data_to_keep)]
        df_cols = dataframe.columns
        column_dict = {dc: ix for ix, dc in enumerate(df_cols)}
        cols = {dc[0]: ix for ix, dc in enumerate(df_cols)}
        drop_data = [ix for col, ix in cols.items() if col not in data]

        drop_cols = []
        for ix, col in enumerate(df_cols):
            if ix in drop_data:
                drop_cols.append(col)

        dataframe.drop(drop_cols, axis=1, inplace=True)

        preview = input("'p' for preview, Enter to continue")
        if preview == 'p':
            print(dataframe.head())
        if preview == "":
            pass
        return dataframe

def save_locally(df):
    path_input = input("path and csv file name\n")
    path = path_input.split(' ')[0]
    file_name = path_input.split(' ')[1]
    df.to_csv("{path}{file_name}.csv".format(path=path, file_name=file_name))

def print_instructions():
    print("Instructions")

alpha_vantage_pull()

def prior(api_key):
    if request_again == True:
        tickers = update_ticks()

    else:
        with open('SP500quotes.pickle', 'rb') as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    else:
        print('Directory Exists')

    for stock in tickers:
        if not exists('SP500/{}.csv'.format(stock)):
            try:
                ts = TimeSeries(key=api_key,
                                output_format='pandas')
                ticker, meta_data = ts.get_daily(symbol=stock,
                                                 outputsize="full")
                ticker = ticker.iloc[2500:]
                drop_labs = [
                    'open',
                    'high',
                    'low',
                    'volume',
                ]
                ticker.drop(drop_labs, axis=1, inplace=True)
                ticker.rename(columns={'close':stock}, inplace=True)
                if ticker.empty:
                    print("Empty dataframe for {} - will not add to stocks_dfs dir".format(stock))
                else:
                    ticker.to_csv('stock_dfs/{}.csv'.format(stock))
                    print("Adding {} to stock_dfs directory".format(stock))
            except:
                s = "Error: {}".format(sys.exc_info()[0])
                s += "\nwhile fetching data for {}".format(stock)