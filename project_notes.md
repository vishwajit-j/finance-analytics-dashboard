# Finance Analytics Dashboard – Project Notes

## Current Architecture

- data_loader.py → Handles multi-asset OHLC data loading
- metrics.py → Calculates:
    - Daily returns
    - Annualized return
    - Annualized volatility
    - Rolling volatility
    - Maximum drawdown
- plots.py → Handles visualization
- app.py → Orchestrates full pipeline

## Implemented Features

- Multi-asset return calculation
- Correlation matrix computation
- Portfolio daily return calculation
- Portfolio annual return & volatility
- Sharpe ratio calculation
- Brute-force Sharpe maximization (weight sweep)
- Best weight detection logic

## Key Result (2-Asset Case)

Optimal Weights:
- AAPL ≈ 0.79
- MSFT ≈ 0.21

Sharpe Ratio ≈ 0.8274

## Observations

- Diversification reduced volatility slightly.
- High correlation (~0.75) limits diversification benefit.
- Optimized portfolio slightly improves Sharpe vs 50/50.

## Next Refactor Goal

- Remove hardcoded 2-asset assumption
- Generalize optimizer for N assets
- Move optimizer into dedicated portfolio module
- Improve modular structure


## Portfolio Optimization (Monte Carlo Simulation)

### What Was Implemented

- Monte Carlo portfolio optimization using random weight generation
- Weight normalization to ensure full capital allocation (sum of weights = 1)
- Sharpe Ratio maximization as optimization objective
- Efficient Frontier visualization (Risk vs Return scatter plot)
- Highlighting optimal Sharpe portfolio on the frontier

### System Architecture

- `data_loader.py` → Data fetching and preprocessing
- `metrics.py` → Financial calculations (returns, volatility, correlation, Sharpe, etc.)
- `portfolio.py` → Optimization logic (Monte Carlo simulation)
- `plots.py` → Visualization layer (Efficient Frontier)
- `app.py` → Controller / orchestration layer

Separation of concerns was enforced to maintain clean modular structure.

### Key Observations & Insights

- Efficient Frontier shape is determined by asset return, volatility, and correlation — not by risk-free rate.
- Changing the risk-free rate does not change the frontier shape but can shift the optimal Sharpe portfolio.
- Maximum Sharpe portfolio is not necessarily the highest return portfolio.
- High return without volatility control leads to lower risk-adjusted performance.
- Diversification benefits arise from lower correlation between assets.

### Architectural Improvements

- Removed financial calculations from `app.py`
- Centralized statistical computations inside `metrics.py`
- Isolated optimization logic inside `portfolio.py`
- Maintained plotting logic strictly inside `plots.py`
- Established clean, scalable backend structure for future extensions (constraints, efficient frontier refinement, additional metrics)


### Portfolio Engine Enhancements

- Added Minimum Volatility portfolio tracking
- Added Maximum Return portfolio tracking
- Implemented Sortino ratio optimization
- Extended return structure from optimize_portfolio()
- Verified architecture separation:
  - metrics → calculations
  - portfolio → optimization logic
  - plots → visualization
  - app → controller

## Observation:
- Max Return portfolio ≠ Max Sharpe
- Sortino portfolio can differ due to downside-only risk penalization


📅 Update — Phase 2 Progress
✅ Today’s Progress

Expanded asset universe to multi-asset portfolio:

US Equity, International Equity, Bonds, Commodities, Energy, Crypto

Implemented full Out-of-Sample (OOS) evaluation framework

Added Walk-Forward Optimization (rolling re-training & testing)

Integrated advanced risk metrics:

Sharpe, Sortino, Calmar

VaR / CVaR

Maximum Drawdown

Added Relative Performance analytics:

Beta, Alpha

Information Ratio

CAPM Regression (OLS summary)

Preserved clean modular architecture:

metrics.py → calculations

portfolio.py → optimization logic

plots.py → visualization

app.py → orchestration

The system is now a multi-asset, risk-evaluated portfolio engine with OOS validation and walk-forward robustness testing.

🔜 Next Steps (Phase 3)

Rolling Beta (time-varying market exposure)

Risk Contribution analysis (volatility attribution per asset)

Correlation heatmap visualization

Further robustness diagnostics

Goal: Upgrade from optimizer → full quantitative risk analytics system.