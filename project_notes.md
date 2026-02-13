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
