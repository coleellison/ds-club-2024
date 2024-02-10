import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
from datetime import date, timedelta
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


yf.pdr_override() #outputs data as a pandas dataframe

def calc_dates(daydelta):
    """calculates start_date and end_date

    Parameters
    ----------
    daydelta : int
        length of stock history

    Returns
    -------
    tuple
        start date and end date, formatted as a string ""YYYY-MM-DD"
    """
    end_date = date.today()
    start_date = end_date - timedelta(days = daydelta)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    return (start_date, end_date)

def price_history(tickers, daydelta):
    """queries yahoo finance for stock history

    Parameters
    ----------
    tickers : list
        list of ticker names
    daydelta : int
        length of time to pull history

    Returns
    -------
    tuple
        dates and historical closing value of the stocks.
    """
    start_date, end_date = calc_dates(daydelta)
    closes = [] #store the closing numbers for stocks daily
    for ticker in tickers:
        data = pdr.get_data_yahoo(ticker, start = start_date, end = end_date) #query yahoo finance api
        data = data.reset_index()
        close = data.drop(["Open", "High", "Low", "Adj Close", "Volume"], axis = 1)
        closes.append(close)
    return closes

def plot_stocks(tickers, daydelta):
    """plots stocks using matplotlib.pyplot

    Parameters
    ----------
    tickers : list
        list of ticker names
    daydelta : int
        length of time to pull history
    """
    closes = price_history(tickers, daydelta) #get the stock history
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y')) #date formatting
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    for stock in closes: #plot each stock
        plt.plot(stock["Date"], stock["Close"])
    plt.legend(tickers) #creates a legend to distinguish different tickers
    if daydelta > 14: #avoid a cluttered x-axis
        plt.xticks(visible = False)
    plt.gcf().autofmt_xdate() #date formatting
    plt.show()
