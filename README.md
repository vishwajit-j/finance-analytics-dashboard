# Portfolio Analytics & Optimization Dashboard

## Overview

This project is an interactive portfolio analytics dashboard designed to analyze investment portfolios from both performance and risk perspectives.

Instead of focusing only on returns, the system provides a structured way to understand:

* how a portfolio grows over time
* how risk is distributed across assets
* how different optimization strategies affect outcomes

It combines financial modeling, data analysis, and an interactive interface into a single system.

---

## Purpose

The goal of this project is to move beyond basic return analysis and provide a more complete view of portfolio behavior.

In typical scenarios, portfolios are evaluated only on returns. However, this can be misleading because:

* high returns may come with concentrated risk
* diversification may appear present but not be effective
* volatility and drawdowns are often ignored

This dashboard addresses these issues by integrating risk-aware metrics and visualization.

---

## What the System Does

The system allows users to:

* select a set of assets
* choose a portfolio construction strategy
* analyze performance over a selected time period

Based on the inputs, it computes and visualizes:

### Performance

* growth of $1 invested
* drawdown (loss from peak)

This helps in understanding both return and stability.

---

### Risk Analysis

* asset-level risk contribution
* correlation between assets

This shows which assets drive portfolio risk and whether diversification is effective.

---

### Portfolio Optimization

* maximum Sharpe ratio portfolio
* minimum volatility portfolio
* maximum return portfolio
* efficient frontier (risk vs return trade-off)

This allows comparison between different portfolio choices rather than relying on a single allocation.

---

### Strategy Comparison

Two approaches are implemented:

**1. Max Sharpe Strategy**

* focuses on maximizing risk-adjusted return
* may concentrate risk in certain assets

**2. Risk Parity Strategy**

* distributes risk more evenly across assets
* often results in more stable portfolios

---

## System Workflow

The system follows a structured pipeline:

1. Load historical price data
2. Compute daily returns
3. Split data into training and testing periods
4. Optimize portfolio weights on training data
5. Evaluate performance on unseen (test) data
6. Visualize results through the dashboard

This ensures that results are not based on overfitting.

---

## Interface (Dashboard)

The dashboard is built using Streamlit and organized into four sections:

### Overview

* portfolio allocation
* summary metrics

### Performance

* portfolio growth over time
* drawdown visualization

### Risk

* risk contribution of each asset
* correlation heatmap

### Optimization

* efficient frontier
* comparison of portfolio choices

The interface allows dynamic interaction through:

* asset selection
* date range filtering
* strategy switching

---

## Key Concepts Used

This project implements several important financial concepts:

* Sharpe Ratio
* Sortino Ratio
* Calmar Ratio
* Efficient Frontier
* Risk Contribution
* Value at Risk (VaR)
* Conditional VaR (CVaR)
* CAPM (Beta, Alpha)

---

## Key Observations

Some consistent patterns observed during testing:

* highest return portfolios often have concentrated risk
* diversification depends more on correlation than number of assets
* risk parity produces more balanced portfolios
* lower volatility portfolios tend to have smoother drawdowns

---

## Limitations

* uses historical data only (no live data)
* assumes constant risk-free rate
* transaction costs and slippage are not considered
* rebalancing is not dynamically modeled

---

## Future Improvements

* integration with live market data
* portfolio rebalancing simulation
* factor analysis (market exposure, sector exposure)
* deployment for public access

---

## Project Structure

```id="m19o2n"
data_loader.py   → data fetching
metrics.py       → financial calculations
portfolio.py     → optimization logic
plots.py         → visualization
dashboard.py     → interactive interface
```

---

## Conclusion

This project started as a basic return analysis script and evolved into a structured portfolio analytics system.

The focus was not only on implementing financial formulas, but also on understanding:

* how portfolios behave under different conditions
* how risk is distributed
* how to present insights in a usable way

---

## Author

Vishwajit Jankar
