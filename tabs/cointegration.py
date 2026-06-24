import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.stattools import coint


def show_cointegration():

    if "prices" not in st.session_state:
        st.info("Download data first")
        return

    if "top_corr_pairs" not in st.session_state:
        st.warning("Run Correlation tab first.")
        return

    # =========================
    # Sidebar Settings
    # =========================

    with st.sidebar.expander(
        "Cointegration Settings",expanded=False):

        top_pairs_to_test = st.slider(
            "Number of Pairs to Test",
            min_value=5,
            max_value=50,
            value=10,
            step=5,
            key="cointegration_num_pairs")

        max_pvalue = st.slider(
            "Maximum P-Value",
            min_value=0.01,
            max_value=0.10,
            value=0.05,
            step=0.01,
            key="cointegration_pvalue")

    # =========================
    # Data
    # =========================

    prices = st.session_state["prices"]

    top_pairs = (
        st.session_state["top_corr_pairs"]
        .head(top_pairs_to_test))

    pairs = []

    # =========================
    # Cointegration Tests
    # =========================

    with st.spinner(
        "Running Cointegration Tests..."):

        for _, row in top_pairs.iterrows():

            stock1 = row["Stock 1"]
            stock2 = row["Stock 2"]

            try:

                score, pvalue, _ = coint(
                    prices[stock1],
                    prices[stock2])

                pairs.append([
                    stock1,
                    stock2,
                    row["Correlation"],
                    score,
                    pvalue])

            except Exception:
                continue

    if len(pairs) == 0:
        st.warning("No valid pairs found.")
        return

    # =========================
    # Results Table
    # =========================

    results = pd.DataFrame(
        pairs,
        columns=[
            "Stock 1",
            "Stock 2",
            "Correlation",
            "ADF Statistic",
            "P-Value"])

    st.subheader("Raw Cointegration Results")

    st.dataframe(
        results.sort_values(
            by="P-Value"
        ),
        use_container_width=True
    )

    #results = results[results["P-Value"] <= max_pvalue]

    results = results.sort_values(
        by="P-Value",
        ascending=True)

    if results.empty:
        st.warning(
            "No cointegrated pairs found.")
        return

    results["Correlation"] = (
        results["Correlation"]
        .round(4))

    results["ADF Statistic"] = (
        results["ADF Statistic"]
        .round(4))

    results["P-Value"] = (
        results["P-Value"]
        .round(6))

    results["Cointegrated"] = (
        results["P-Value"] < 0.05)

    # =========================
    # Display
    # =========================

    st.subheader(
        "Cointegrated Pairs")

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True)

    st.metric(
        "Cointegrated Pairs Found",
        len(results))

    # =========================
    # Pair Selection
    # =========================

    pair_options = [
        f"{row['Stock 1']} | {row['Stock 2']}"
        for _, row in results.iterrows()]

    selected_pair = st.selectbox(
        "Select Pair for Spread Analysis",
        pair_options,
        key="cointegration_pair_select")

    stock1, stock2 = selected_pair.split(
        " | ")

    st.session_state["selected_pair"] = (
        stock1,
        stock2)

    st.success(
        f"Selected Pair: {stock1} & {stock2}")

    # =========================
    # Pair Price Chart
    # =========================

    st.subheader(
        "Selected Pair Analysis"
    )

    pair_prices = prices[
        [stock1, stock2]
    ]

    normalized = (
                         pair_prices /
                         pair_prices.iloc[0]
                 ) * 100

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized[stock1],
            mode="lines",
            name=stock1,
            line=dict(width=2)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized[stock2],
            mode="lines",
            name=stock2,
            line=dict(width=2)
        )
    )

    fig.update_layout(
        title="Normalized Price Comparison",
        xaxis_title="Date",
        yaxis_title="Normalized Price (Base = 100)",
        hovermode="x unified",
        height=600,
        legend=dict(
            orientation="h",
            y=1.02,
            x=1,
            xanchor="right"
        ),
        xaxis=dict(
            rangeslider=dict(
                visible=True
            )
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =========================
    # Rolling Spread
    # =========================

    st.subheader(
        "Rolling Spread"
    )

    spread_series = (
            pair_prices[stock1]
            - pair_prices[stock2]
    )

    rolling_spread = (
            spread_series
            - spread_series.rolling(30).mean()
    )

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=rolling_spread.index,
            y=rolling_spread,
            mode="lines",
            name="Spread",
            line=dict(width=2)
        )
    )

    fig2.add_hline(
        y=0,
        line_dash="dash"
    )

    fig2.update_layout(
        title="Rolling Spread (30-Day Mean Removed)",
        xaxis_title="Date",
        yaxis_title="Spread",
        hovermode="x unified",
        height=500,
        xaxis=dict(
            rangeslider=dict(
                visible=True
            )
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )