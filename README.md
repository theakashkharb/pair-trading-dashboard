# Pair Trading Dashboard

A Statistical Arbitrage Research Platform built with Python and Streamlit.

This dashboard allows traders and researchers to discover, analyze, and backtest mean-reverting stock pairs using correlation, cointegration, spread analysis, and z-score based trading signals.

---

## Features

### Data & Universe Selection

* Country Selection
* Sector Selection
* Custom Stock Universe
* Historical Data Download via Yahoo Finance

### Pair Discovery

* Correlation Matrix
* Correlation Heatmap
* Top Correlated Pairs Ranking

### Statistical Tests

* Engle-Granger Cointegration Test
* Cointegration P-Value Analysis
* Pair Selection Workflow

### Spread Analysis

* OLS Hedge Ratio Estimation
* Spread Construction
* Half-Life Estimation
* Mean Reversion Analysis

### Signal Generation

* Rolling Z-Score Calculation
* Entry Signal Detection
* Exit Signal Detection

### Backtesting

* Strategy Backtest Engine
* Equity Curve
* Trade Signal Visualization
* Performance Evaluation

---

## Research Workflow

Stocks Universe

↓

Correlation Screening

↓

Cointegration Testing

↓

Pair Selection

↓

Hedge Ratio Estimation

↓

Spread Construction

↓

Half-Life Estimation

↓

Z-Score Signal Generation

↓

Backtesting

---

## Quantitative Concepts Implemented

* Pearson Correlation
* Cointegration Testing
* Ordinary Least Squares (OLS)
* Hedge Ratio Estimation
* Mean Reversion
* Half-Life Estimation
* Spread Construction
* Z-Score Normalization
* Statistical Arbitrage
* Backtesting

---

## Technology Stack

* Python
* Streamlit
* Pandas
* NumPy
* Plotly
* Statsmodels
* yFinance

---

## Installation

```bash
git clone https://github.com/theakashkharb/pair-trading-dashboard.git

cd pair-trading-dashboard

pip install -r requirements.txt

streamlit run main.py
```

---

## Live Demo

Streamlit App:

(Add your Streamlit URL here)

---

## Current Modules

* Overview
* Correlation
* Cointegration
* Spread Analysis
* Z-Score Analysis
* Backtesting

---

## Roadmap

### Version 2

* Trade Log
* Win Rate
* Profit Factor
* Maximum Drawdown
* Portfolio Backtesting

### Version 3

* Transaction Costs
* Walk-Forward Testing
* Rolling Cointegration
* Portfolio Analytics

### Version 4

* Interactive Brokers Integration
* Live Trading Engine
* Automated Order Execution
* Portfolio Monitoring

---

## Author

Akash Kharb

Quantitative Finance | Algorithmic Trading | Statistical Arbitrage
