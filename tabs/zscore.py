import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def show_zscore():

    if "spread" not in st.session_state:
        st.info("Run Spread tab first")
        return

    spread = st.session_state["spread"]

    with st.sidebar.expander(
        "Z-Score Settings",
        expanded=False
    ):

        lookback = st.slider(
            "Lookback Window",
            min_value=10,
            max_value=100,
            value=30,
            step=5,
            key="zscore_lookback"
        )

        entry_z = st.slider(
            "Entry Z",
            min_value=1.0,
            max_value=3.0,
            value=2.0,
            step=0.1,
            key="zscore_entry"
        )

        exit_z = st.slider(
            "Exit Z",
            min_value=0.0,
            max_value=1.5,
            value=0.5,
            step=0.1,
            key="zscore_exit"
        )

    # =========================
    # Z-Score
    # =========================

    rolling_mean = spread.rolling(
        lookback
    ).mean()

    rolling_std = spread.rolling(
        lookback
    ).std()

    zscore = (
                     spread - rolling_mean
             ) / rolling_std

    zscore = zscore.dropna()

    if zscore.empty:
        st.warning(
            "Not enough data for current lookback window."
        )
        return

    current_z = zscore.iloc[-1]

    # =========================
    # Signal
    # =========================

    if current_z > entry_z:

        signal = "SHORT SPREAD"

    elif current_z < -entry_z:

        signal = "LONG SPREAD"

    elif abs(current_z) < exit_z:

        signal = "EXIT"

    else:

        signal = "NO TRADE"

    # =========================
    # Metrics
    # =========================

    st.subheader(
        "Z-Score Analysis"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Current Z-Score",
        round(current_z, 2)
    )

    col2.metric(
        "Signal",
        signal
    )

    # =========================
    # Z-Score Chart
    # =========================

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=zscore.index,
            y=zscore,
            name="Z-Score",
            mode="lines",
            line=dict(width=2)
        )
    )

    fig.add_hline(
        y=0,
        annotation_text="Mean"
    )

    fig.add_hline(
        y=entry_z,
        line_dash="dash",
        annotation_text=f"+{entry_z}"
    )

    fig.add_hline(
        y=-entry_z,
        line_dash="dash",
        annotation_text=f"-{entry_z}"
    )

    fig.add_hline(
        y=exit_z,
        line_dash="dot"
    )

    fig.add_hline(
        y=-exit_z,
        line_dash="dot"
    )

    fig.update_layout(
        title="Rolling Z-Score",
        hovermode="x unified",
        height=650,
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
    # Signal History
    # =========================

    signals = pd.DataFrame(
        {
            "Z-Score": zscore
        }
    )

    signals["Signal"] = np.where(
        signals["Z-Score"] > entry_z,
        "Short Spread",
        np.where(
            signals["Z-Score"] < -entry_z,
            "Long Spread",
            "No Signal"
        )
    )

    st.subheader(
        "Recent Signals"
    )

    st.dataframe(
        signals.tail(20),
        use_container_width=True
    )

    st.session_state["zscore"] = zscore
    st.session_state["current_signal"] = signal