import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import numpy as np


def show_spread():

    if "prices" not in st.session_state:
        st.info("Download data first")
        return

    if "selected_pair" not in st.session_state:
        st.info("Select a pair in Cointegration tab")
        return

    # =========================
    # Data
    # =========================

    prices = st.session_state["prices"]

    stock1, stock2 = st.session_state["selected_pair"]

    y = prices[stock1]
    x = prices[stock2]

    # =========================
    # Hedge Ratio
    # =========================

    x_const = sm.add_constant(x)

    model = sm.OLS(
        y,
        x_const
    ).fit()

    beta = model.params.iloc[1]

    # =========================
    # Spread
    # =========================

    spread = y - beta * x

    st.session_state["spread"] = spread
    st.session_state["hedge_ratio"] = beta

    # =========================
    # Half Life
    # =========================

    spread_lag = spread.shift(1)

    spread_ret = spread - spread_lag

    spread_df = pd.concat(
        [spread_lag, spread_ret],
        axis=1
    ).dropna()

    spread_df.columns = [
        "lag",
        "delta"
    ]

    X = sm.add_constant(
        spread_df["lag"]
    )

    hl_model = sm.OLS(
        spread_df["delta"],
        X
    ).fit()

    gamma = hl_model.params.iloc[1]

    if gamma < 0:

        halflife = (
            -np.log(2) / gamma
        )

    else:

        halflife = np.nan

    st.session_state["half_life"] = halflife

    # =========================
    # Current Z
    # =========================

    spread_mean = spread.mean()
    spread_std = spread.std()

    current_z = (
        spread.iloc[-1] - spread_mean
    ) / spread_std

    # =========================
    # Metrics
    # =========================

    st.subheader(
        "Spread Analysis"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Stock 1",
        stock1
    )

    col2.metric(
        "Stock 2",
        stock2
    )

    col3.metric(
        "Hedge Ratio β",
        round(beta, 4)
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Spread Mean",
        round(
            spread_mean,
            4
        )
    )

    if np.isnan(halflife):

        col2.metric(
            "Half Life",
            "N/A"
        )

    else:

        col2.metric(
            "Half Life",
            round(
                halflife,
                2
            )
        )

    col3.metric(
        "Current Z",
        round(
            current_z,
            2
        )
    )

    # =========================
    # Signal Preview
    # =========================

    if current_z > 2:

        st.error(
            "Signal: Short Spread"
        )

    elif current_z < -2:

        st.success(
            "Signal: Long Spread"
        )

    else:

        st.info(
            "Signal: No Trade"
        )

    # =========================
    # Normalized Prices
    # =========================

    st.subheader(
        "Normalized Price Comparison"
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
            name=stock1,
            mode="lines",
            line=dict(width=2)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized[stock2],
            name=stock2,
            mode="lines",
            line=dict(width=2)
        )
    )

    fig.update_layout(
        title="Normalized Price Comparison",
        hovermode="x unified",
        height=550,
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
    # Spread Chart
    # =========================

    st.subheader(
        "Spread"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=spread.index,
            y=spread,
            name="Spread",
            mode="lines",
            line=dict(width=2)
        )
    )

    fig.add_hline(
        y=spread_mean,
        annotation_text="Mean"
    )

    fig.add_hline(
        y=spread_mean + spread_std,
        line_dash="dot"
    )

    fig.add_hline(
        y=spread_mean - spread_std,
        line_dash="dot"
    )

    fig.add_hline(
        y=spread_mean + 2 * spread_std,
        line_dash="dash",
        annotation_text="+2σ"
    )

    fig.add_hline(
        y=spread_mean - 2 * spread_std,
        line_dash="dash",
        annotation_text="-2σ"
    )

    fig.update_layout(
        title="Spread with Standard Deviation Bands",
        hovermode="x unified",
        height=600,
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
    # Spread Distribution
    # =========================

    st.subheader(
        "Spread Distribution"
    )

    fig = px.histogram(
        spread,
        nbins=50,
        marginal="box",
        title="Spread Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =========================
    # Interpretation
    # =========================

    if not np.isnan(halflife):

        if halflife < 5:

            st.warning(
                "Very fast mean reversion."
            )

        elif halflife < 30:

            st.success(
                "Good mean reversion."
            )

        elif halflife < 60:

            st.info(
                "Moderate mean reversion."
            )

        else:

            st.error(
                "Slow mean reversion."
            )