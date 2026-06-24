import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def show_backtest():

    if "zscore" not in st.session_state:
        st.info("Run Z-Score tab first")
        return

    if "spread" not in st.session_state:
        st.info("Run Spread tab first")
        return

    zscore = st.session_state["zscore"]
    spread = st.session_state["spread"]

    with st.sidebar.expander(
        "Backtest Settings",
        expanded=False
    ):

        entry_z = st.slider(
            "Entry Z",
            1.0,
            3.0,
            2.0,
            0.1,
            key="bt_entry"
        )

        exit_z = st.slider(
            "Exit Z",
            0.0,
            1.5,
            0.5,
            0.1,
            key="bt_exit"
        )

    signals = pd.Series(
        0,
        index=zscore.index
    )

    signals[zscore > entry_z] = -1
    signals[zscore < -entry_z] = 1

    position = 0

    positions = []

    for z in zscore:

        if position == 0:

            if z > entry_z:
                position = -1

            elif z < -entry_z:
                position = 1

        else:

            if abs(z) < exit_z:
                position = 0

        positions.append(position)

    positions = pd.Series(
        positions,
        index=zscore.index
    )

    spread_returns = (
        spread.diff()
        .reindex(zscore.index)
    )

    pnl = (
        positions.shift(1)
        * spread_returns
    )

    pnl = pnl.fillna(0)

    equity = pnl.cumsum()

    # =========================
    # Metrics
    # =========================

    total_return = equity.iloc[-1]

    num_trades = (
        positions.diff()
        .abs()
        .sum()
        / 2
    )

    sharpe = (
        pnl.mean()
        / pnl.std()
        * np.sqrt(252)
        if pnl.std() > 0
        else 0
    )

    st.subheader(
        "Backtest Metrics"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total PnL",
        round(total_return, 2)
    )

    col2.metric(
        "Sharpe Ratio",
        round(sharpe, 2)
    )

    col3.metric(
        "Trades",
        int(num_trades)
    )

    # =========================
    # Equity Curve
    # =========================

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=equity.index,
            y=equity,
            mode="lines",
            name="Equity"
        )
    )

    fig.update_layout(
        title="Equity Curve",
        hovermode="x unified",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =========================
    # Position Chart
    # =========================

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=positions.index,
            y=positions,
            mode="lines",
            name="Position"
        )
    )

    fig2.update_layout(
        title="Position History",
        height=400
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )