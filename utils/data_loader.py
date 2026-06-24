import pandas as pd
import yfinance as yf
import datetime as dt


def load_stock_list():

    stocks = pd.read_csv("Stocks.csv")

    return stocks


def download_prices(
        tickers,
        start_date,
        end_date):

    end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1)

    prices = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        multi_level_index=False
    )["Adj Close"]

    return prices


def calculate_returns(prices):

    returns = prices.pct_change()

    return returns


def clean_data(df):

    return df.dropna()