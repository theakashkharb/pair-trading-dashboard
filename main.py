import streamlit as st
import pandas as pd

from utils.data_loader import download_prices

from tabs.overview import show_overview
from tabs.correlation import show_correlation
from tabs.comparison import show_comparison
from tabs.cointegration import show_cointegration
from tabs.spread import show_spread
from tabs.zscore import show_zscore


st.set_page_config(
    page_title="Pair Trading Dashboard",
    layout="wide"
)

# Sidebar
st.sidebar.title("Select Asset")

data = pd.read_csv("/Users/akash/PycharmProjects/"
                   "pair-trading-dashboard/fno.csv")

stocks = data["ticker"].tolist()

selected_stocks = st.sidebar.multiselect(
    "Select Option",
    stocks
)

start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

download_btn = st.sidebar.button("Download Data")


if download_btn:

    if len(selected_stocks) < 2:
        st.error("Please select at least two stocks")
        st.stop()

    filtered = data[
        data["ticker"].isin(selected_stocks)
    ]

    yf_tickers = filtered["yf_ticker"].tolist()

    with st.spinner("Downloading Data..."):

        prices = download_prices(
            yf_tickers,
            start_date,
            end_date
        )

    mapping = dict(
        zip(
            filtered["yf_ticker"],
            filtered["ticker"]
        )
    )

    prices = prices.rename(columns=mapping)

    prices = prices.dropna()

    if len(prices) == 0:
        st.error("No data found")
        st.stop()

    prices.index = prices.index.date

    returns = prices.pct_change().dropna()

    st.session_state["prices"] = prices
    st.session_state["returns"] = returns


(
    overview_tab,
    corr_tab,
    comparison_tab,
    cointegration_tab,
    spread_tab,
    z_tab
) = st.tabs([
    "Overview",
    "Correlation",
    "Comparison",
    "Cointegration",
    "Spread",
    "Z-Score"
])


with overview_tab:
    show_overview()

with corr_tab:
    show_correlation()

with comparison_tab:
    pass

with cointegration_tab:
    pass

with spread_tab:
    pass

with z_tab:
    pass