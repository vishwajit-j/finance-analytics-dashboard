from data_loader import load_data
from metrics import (
    calculate_daily_returns,
    calculate_correlation_matrix,
)
from portfolio import optimize_portfolio
from plots import plot_efficient_frontier
import numpy as np
from metrics import calculate_portfolio_drawdown



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
    min_vol_weights,
    min_volatility,
    min_return,
    max_return_weights,
    max_return,
    max_vol,
    best_sortino_weights,
    best_sortino,
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

    print("\nMinimum Volatility Portfolio:")
    for ticker, weight in zip(returns.columns, min_vol_weights):
        print(f"{ticker}: {weight:.4f}")
    print(f"Volatility: {min_volatility:.4f}")

    print("\nMaximum Return Portfolio:")
    for ticker, weight in zip(returns.columns, max_return_weights):
        print(f"{ticker}: {weight:.4f}")
    print(f"Return: {max_return:.4f}")

    print("\nBest Sortino Portfolio:")
    for ticker, weight in zip(returns.columns, best_sortino_weights):
        print(f"{ticker}: {weight:.4f}")

    print(f"Sortino Ratio: {best_sortino:.4f}")



    # Best Sharpe portfolio returns
    best_portfolio_returns = returns.dot(best_weights)
    best_drawdown = calculate_portfolio_drawdown(best_portfolio_returns)

    # Minimum volatility portfolio returns
    min_portfolio_returns = returns.dot(min_vol_weights)
    min_drawdown = calculate_portfolio_drawdown(min_portfolio_returns)

    # Maximum return portfolio returns
    max_portfolio_returns = returns.dot(max_return_weights)
    max_drawdown = calculate_portfolio_drawdown(max_portfolio_returns)

    print("\nMaximum Drawdowns:")

    print(f"Max Sharpe Portfolio Drawdown: {best_drawdown:.4f}")
    print(f"Min Volatility Portfolio Drawdown: {min_drawdown:.4f}")
    print(f"Max Return Portfolio Drawdown: {max_drawdown:.4f}")


    plot_efficient_frontier(
    all_volatilities,
    all_returns,
    all_sharpes,
    best_vol,
    best_return,
    min_volatility,
    min_return,
    max_vol,
    max_return)


if __name__ == "__main__":
    main()
