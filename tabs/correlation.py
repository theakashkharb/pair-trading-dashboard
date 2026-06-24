import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def show_correlation():

    if "returns" not in st.session_state:
        st.info("Download data first")
        return

    # =========================
    # Sidebar Controls
    # =========================

    # =========================
    # Sidebar Controls
    # =========================

    with st.sidebar.expander(
            "Correlation Settings",
            expanded=False
    ):

        corr_threshold = st.slider(
            "Minimum Correlation",
            min_value=0.50,
            max_value=1.00,
            value=0.80,
            step=0.01
        )

        top_n = st.slider(
            "Top N Pairs",
            min_value=10,
            max_value=100,
            value=25,
            step=5
        )

        show_matrix = st.checkbox(
            "Show Correlation Matrix",
            value=False
        )

        show_heatmap = st.checkbox(
            "Show Heatmap",
            value=False
        )

    # =========================
    # Data
    # =========================

    returns = st.session_state["returns"]

    corr_matrix = returns.corr()

    # =========================
    # Correlation Matrix
    # =========================

    if show_matrix:

        st.subheader("Correlation Matrix")

        st.dataframe(
            corr_matrix.round(2),
            use_container_width=True
        )

    # =========================
    # Correlation Heatmap
    # =========================

    if show_heatmap:

        st.subheader("Correlation Heatmap")

        fig = px.imshow(
            corr_matrix,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdYlGn",
            zmin=-1,
            zmax=1
        )

        fig.update_layout(
            height=700
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =========================
    # Top Correlated Pairs
    # =========================

    st.subheader("Top Correlated Pairs")

    pairs = []

    for i in range(len(corr_matrix.columns)):

        for j in range(i + 1, len(corr_matrix.columns)):

            stock1 = corr_matrix.columns[i]
            stock2 = corr_matrix.columns[j]

            corr_value = corr_matrix.iloc[i, j]

            pairs.append([
                stock1,
                stock2,
                corr_value
            ])

    pairs_df = pd.DataFrame(
        pairs,
        columns=[
            "Stock 1",
            "Stock 2",
            "Correlation"
        ]
    )

    pairs_df = pairs_df.sort_values(
        by="Correlation",
        ascending=False
    )
    pairs_df = pd.DataFrame(
        pairs,
        columns=[
            "Stock 1",
            "Stock 2",
            "Correlation"
        ]
    )

    pairs_df = pairs_df.sort_values(
        by="Correlation",
        ascending=False
    )

    st.session_state["top_corr_pairs"] = pairs_df.copy()

    pairs_df = pairs_df[
        pairs_df["Correlation"] >= corr_threshold
        ]

    pairs_df = pairs_df[
        pairs_df["Correlation"] >= corr_threshold
    ]

    pairs_df = pairs_df.head(top_n)

    pairs_df["Correlation"] = (
        pairs_df["Correlation"]
        .round(4)
    )

    st.dataframe(
        pairs_df,
        use_container_width=True,
        hide_index=True
    )