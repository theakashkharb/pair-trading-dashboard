import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd


def show_overview():

    if "prices" not in st.session_state:
        st.info("Download data first")
        return

    prices = st.session_state["prices"]
    returns = st.session_state["returns"]

    # =========================
    # Summary Metrics
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Stocks", len(prices.columns))

    col2.write("**Start Date**")
    col2.write(prices.index[0])

    col3.write("**End Date**")
    col3.write(prices.index[-1])

    col4.metric("Trading Days", len(prices))

    st.divider()

    # =========================
    # Performance Table
    # =========================

    overview = []

    for stock in prices.columns:

        latest_price = prices[stock].iloc[-1]

        month_return = np.nan

        if len(prices) >= 22:
            month_return = (
                prices[stock].iloc[-1]
                / prices[stock].iloc[-22]
                - 1
            ) * 100

        current_year = prices.index[-1].year

        ytd_start = prices[stock][
            [d.year == current_year for d in prices.index]
        ].iloc[0]

        ytd_return = (
            prices[stock].iloc[-1]
            / ytd_start
            - 1
        ) * 100

        volatility = (
            prices[stock]
            .pct_change()
            .std()
            * np.sqrt(252)
            * 100
        )

        overview.append({
            "Ticker": stock,
            "Price": round(latest_price, 2),
            "Month %": round(month_return, 2),
            "YTD %": round(ytd_return, 2),
            "Volatility %": round(volatility, 2)
        })

    overview_df = pd.DataFrame(overview)

    overview_df = overview_df.sort_values(
        by="Month %",
        ascending=False
    )

    st.subheader("Performance Summary")

    st.dataframe(
        overview_df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # Normalized Price Chart
    # =========================

    st.subheader("Normalized Price Comparison")

    normalized = prices.div(prices.iloc[0]) * 100

    fig = px.line(
        normalized,
        title="Normalized Price Comparison"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Date",
        yaxis_title="Normalized Price"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =========================
    # Return Distribution
    # =========================

    st.subheader("Return Distribution")

    returns_long = returns.stack().reset_index(drop=True)

    fig = px.histogram(
        returns_long,
        nbins=50,
        title="Distribution of Daily Returns"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Daily Return",
        yaxis_title="Frequency"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )