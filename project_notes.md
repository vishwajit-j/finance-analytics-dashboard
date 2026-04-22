# Finance Analytics Dashboard – Project Notes

## Current Architecture

* data_loader.py → Handles multi-asset OHLC data loading
* metrics.py → Calculates:

  * Daily returns
  * Annualized return
  * Annualized volatility
  * Rolling volatility
  * Maximum drawdown
* plots.py → Handles visualization
* app.py / dashboard.py → Orchestrates full pipeline and UI

---

## Implemented Features

* Multi-asset return calculation
* Correlation matrix computation
* Portfolio daily return calculation
* Portfolio annual return & volatility
* Sharpe ratio calculation
* Brute-force Sharpe maximization (weight sweep)
* Best weight detection logic

---

## Key Result (2-Asset Case)

Optimal Weights:

* AAPL ≈ 0.79
* MSFT ≈ 0.21

Sharpe Ratio ≈ 0.8274

---

## Observations

* Diversification reduced volatility slightly.
* High correlation (~0.75) limits diversification benefit.
* Optimized portfolio slightly improves Sharpe vs 50/50.

---

## Next Refactor Goal

* Remove hardcoded 2-asset assumption
* Generalize optimizer for N assets
* Move optimizer into dedicated portfolio module
* Improve modular structure

---

## Portfolio Optimization (Monte Carlo Simulation)

### What Was Implemented

* Monte Carlo portfolio optimization using random weight generation
* Weight normalization to ensure full capital allocation (sum of weights = 1)
* Sharpe Ratio maximization as optimization objective
* Efficient Frontier visualization (Risk vs Return scatter plot)
* Highlighting optimal Sharpe portfolio on the frontier

### System Architecture

* `data_loader.py` → Data fetching and preprocessing
* `metrics.py` → Financial calculations (returns, volatility, correlation, Sharpe, etc.)
* `portfolio.py` → Optimization logic (Monte Carlo simulation)
* `plots.py` → Visualization layer (Efficient Frontier)
* `app.py` → Controller / orchestration layer

Separation of concerns was enforced to maintain clean modular structure.

### Key Observations & Insights

* Efficient Frontier shape is determined by asset return, volatility, and correlation — not by risk-free rate.
* Changing the risk-free rate does not change the frontier shape but can shift the optimal Sharpe portfolio.
* Maximum Sharpe portfolio is not necessarily the highest return portfolio.
* High return without volatility control leads to lower risk-adjusted performance.
* Diversification benefits arise from lower correlation between assets.

### Architectural Improvements

* Removed financial calculations from `app.py`
* Centralized statistical computations inside `metrics.py`
* Isolated optimization logic inside `portfolio.py`
* Maintained plotting logic strictly inside `plots.py`
* Established clean, scalable backend structure for future extensions

---

## Portfolio Engine Enhancements

* Added Minimum Volatility portfolio tracking
* Added Maximum Return portfolio tracking
* Implemented Sortino ratio optimization
* Extended return structure from optimize_portfolio()

### Observation

* Max Return portfolio ≠ Max Sharpe
* Sortino portfolio differs due to downside-only risk penalization

---

## Phase 2 — Multi-Asset System & Advanced Metrics

### What Was Implemented

* Expanded asset universe:

  * US Equity
  * International Equity
  * Bonds
  * Commodities
  * Energy
  * Crypto

* Implemented Out-of-Sample (OOS) evaluation:

  * Train/Test split
  * Forward validation

* Added Walk-Forward Optimization:

  * Rolling training and testing windows

* Integrated advanced risk metrics:

  * Sharpe ratio
  * Sortino ratio
  * Calmar ratio
  * Value at Risk (VaR)
  * Conditional VaR (CVaR)
  * Maximum drawdown

* Added relative performance metrics:

  * Beta
  * Alpha
  * Information ratio

* Implemented CAPM regression:

  * OLS summary output

### System State

The system evolved into a multi-asset portfolio engine with:

* Risk-adjusted evaluation
* Out-of-sample validation
* Walk-forward robustness testing

---

## Phase 3 — Risk Decomposition & Diagnostics

### Risk Contribution Analysis

#### What Was Implemented

* Covariance-based portfolio risk decomposition
* Asset-level contribution to total portfolio volatility
* Percentage contribution normalization

#### Purpose

* Identify which assets dominate risk
* Evaluate diversification effectiveness

#### Observations

* High-volatility assets dominate risk even with moderate weights
* Risk contribution is not proportional to weight
* Negative contributions appear due to correlation (hedging effect)

---

### Correlation Heatmap

#### What Was Implemented

* Full correlation matrix visualization
* Heatmap representation (-1 to +1 scale)

#### Purpose

* Understand inter-asset relationships
* Identify diversification opportunities

#### Observations

* Equities are highly correlated
* Bonds and Gold act as partial hedges
* Crypto shows low correlation with traditional assets

---

## Phase 4 — Dashboard Integration (Streamlit)

### What Was Implemented

* Interactive dashboard using Streamlit

* Sidebar controls:

  * Asset selection
  * Strategy selection
  * Date range filtering

* Tab-based layout:

  * Overview
  * Performance
  * Risk
  * Optimization

### Architecture Shift

* Transition from script execution → interactive system
* User inputs dynamically drive backend calculations

---

### Performance Visualization

* Portfolio growth curve (Growth of $1)
* Drawdown visualization

#### Observations

* Higher return portfolios show larger drawdowns
* Stable portfolios show smoother growth

---

### Risk Visualization

* Risk contribution bar chart integrated into dashboard
* Dynamic updates based on selected assets

---

### Optimization Visualization

* Efficient Frontier embedded in dashboard
* Highlights:

  * Max Sharpe portfolio
  * Minimum volatility portfolio
  * Maximum return portfolio

---

## Phase 5 — Strategy Expansion

### Risk Parity Portfolio

#### What Was Implemented

* Equal risk contribution-based optimization
* Implemented using constrained optimization (SciPy)

#### Purpose

* Compare weight-based vs risk-based allocation

#### Observations

* Produces more balanced risk distribution
* Allocates higher weight to low-volatility assets
* Provides more stable drawdown behavior in some scenarios

---

## Phase 6 — System Stability & Refinement

### Issues Encountered

* Empty datasets for certain date ranges
* Invalid inputs causing runtime failures
* Plot scaling and readability issues
* UI inconsistency across components

---

### Fixes Applied

* Input validation:

  * Minimum asset selection
  * Valid date range enforcement

* Default values for stability

* Standardized chart sizes and layouts

* Improved UI responsiveness

---

## Final System Capabilities

* Multi-asset portfolio optimization
* Risk-adjusted performance evaluation
* Out-of-sample and walk-forward validation
* Risk decomposition (contribution analysis)
* Correlation analysis
* Strategy comparison (Max Sharpe vs Risk Parity)
* Interactive dashboard with real-time controls

---

## Overall System Evolution

Initial:

* Basic return calculations
* 2-asset optimization

Intermediate:

* Multi-asset optimization
* Efficient frontier modeling

Advanced:

* Risk analytics and diagnostics
* Walk-forward validation

Final:

* Interactive portfolio analytics dashboard

---

## Key Takeaways

* Portfolio optimization requires both return and risk analysis
* Risk contribution provides deeper insight than total volatility
* Correlation structure drives diversification
* Clean architecture improves scalability
* UI integration enhances interpretability and usability
