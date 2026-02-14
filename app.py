from data_loader import load_data
from metrics import (
    calculate_daily_returns,
    calculate_correlation_matrix,
)
from portfolio import optimize_portfolio
from plots import plot_efficient_frontier
import numpy as np

def main():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    start_date = "2020-01-01"
    end_date = "2024-12-31"

    # Load Data
    data = load_data(tickers, start_date, end_date)

    returns = calculate_daily_returns(data)
    
    print("Daily Returns:")
    print(returns.head())

    correlation_matrix = calculate_correlation_matrix(returns)

    print("\nCorrelation Matrix:")
    print(correlation_matrix)

    # Portfolio Optimization
    risk_free_rate = 0.04

    
    (
    best_weights,
    best_sharpe,
    all_returns,
    all_volatilities,
    all_sharpes
    ) = optimize_portfolio(
    returns,
    risk_free_rate=risk_free_rate,
    simulations=5000
    )
    

    # Calculate best portfolio performance
    portfolio_returns = returns.dot(best_weights)
    best_return = portfolio_returns.mean() * 252
    best_vol = portfolio_returns.std() * np.sqrt(252)


    print("\nOptimized Portfolio (Monte Carlo):")
    for ticker, weight in zip(returns.columns, best_weights):
        print(f"{ticker}: {weight:.4f}")

    print(f"\nSharpe Ratio: {best_sharpe:.4f}")

    plot_efficient_frontier(
        all_volatilities,
        all_returns,
        all_sharpes,
        best_vol,
        best_return
    )


if __name__ == "__main__":
    main()
