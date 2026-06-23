import pandas as pd
import yfinance as yf


def load_stock_list():

    stocks = pd.read_csv("/Users/akash/PycharmProjects/pair-trading-dashboard/fno.csv")

    return stocks


def download_prices(
        tickers,
        start_date,
        end_date):

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