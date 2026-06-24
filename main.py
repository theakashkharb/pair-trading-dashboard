import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.data_loader import download_prices

from tabs.overview import show_overview
from tabs.correlation import show_correlation
from tabs.cointegration import show_cointegration
from tabs.spread import show_spread
from tabs.zscore import show_zscore
from tabs.backtest import show_backtest


st.set_page_config(
    page_title="Pair Trading Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            min-width: 350px !important;
            max-width: 350px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# Sidebar
# =========================

st.sidebar.title("Select Asset")

data = pd.read_csv(
    "/Users/akash/PycharmProjects/pair-trading-dashboard/Stocks.csv"
)

data.columns = data.columns.str.strip()

data = data.rename(
    columns={
        "Symbol": "ticker"
    }
)

# Create unique display names
data["display_name"] = (
    data["ticker"]
    + " ("
    + data["Country"]
    + ")"
)

# -------------------------
# Country Filter
# -------------------------

with st.sidebar.expander(
    "Data Selection",
    expanded=True
):

    countries = sorted(
        data["Country"].dropna().unique()
    )

    selected_countries = st.multiselect(
        "Country",
        countries
    )

    filtered_data = data.copy()

    if selected_countries:
        filtered_data = filtered_data[
            filtered_data["Country"].isin(
                selected_countries
            )
        ]

    sectors = sorted(
        filtered_data["Sector"].dropna().unique()
    )

    selected_sectors = st.multiselect(
        "Sector",
        sectors
    )

    if selected_sectors:
        filtered_data = filtered_data[
            filtered_data["Sector"].isin(
                selected_sectors
            )
        ]

    stocks = sorted(
        filtered_data["display_name"].tolist()
    )

    selected_stocks = st.multiselect(
        "Select Stocks",
        stocks
    )

    st.write(
        f"{len(stocks)} stocks available"
    )

    start_date = st.date_input(
        "Start Date"
    )

    end_date = st.date_input("End Date")

    download_btn = st.button(
        "Download Data")

# =========================
# Download Data
# =========================

if download_btn:

    if len(selected_stocks) < 2:
        st.error(
            "Please select at least two stocks"
        )
        st.stop()

    filtered = data[
        data["display_name"].isin(
            selected_stocks
        )
    ]

    yf_tickers = filtered[
        "yf_ticker"
    ].tolist()

    with st.spinner(
        "Downloading Data..."
    ):

        prices = download_prices(
            yf_tickers,
            start_date,
            end_date
        )

    mapping = dict(
        zip(
            filtered["yf_ticker"],
            filtered["display_name"]
        )
    )

    prices = prices.rename(
        columns=mapping
    )

    # Optional: safer than dropna()
    prices = prices.ffill()
    prices = prices.dropna(
        axis=1,
        how="all"
    )

    if prices.empty:
        st.error(
            "No data found"
        )
        st.stop()

    prices.index = prices.index.date

    returns = (
        prices
        .pct_change()
        .dropna()
    )

    st.session_state["prices"] = prices
    st.session_state["returns"] = returns

# =========================
# Tabs
# =========================

(
    overview_tab,
    corr_tab,
    cointegration_tab,
    spread_tab,
    z_tab,
    backtest_tab
) = st.tabs(
    [
        "Overview",
        "Correlation",
        "Cointegration",
        "Spread",
        "Z-Score",
        "Backtest",
    ]
)

with overview_tab:
    show_overview()

with corr_tab:
    show_correlation()

with cointegration_tab:
    show_cointegration()

with spread_tab:
    show_spread()

with z_tab:
    show_zscore()

with backtest_tab:
    show_backtest()