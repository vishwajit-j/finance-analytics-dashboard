from data_loader import load_data
from metrics import (
    calculate_daily_returns,
    calculate_annualized_volatility,
    calculate_cumulative_return,
    calculate_rolling_volatility,
    calculate_max_drawdown,
)
from plots import plot_cumulative_return

def main():
    tickers = ["AAPL", "MSFT"]
    start_date = "2020-01-01"
    end_date = "2024-12-31"

    data = load_data(tickers, start_date, end_date)

    # Extract Close prices
    close_prices = data["Close"]

    # Calculate daily returns for each stock
    returns = close_prices.pct_change().dropna()

    print("Daily Returns:")
    print(returns.head())

    # Correlation matrix
    correlation_matrix = returns.corr()

    print("\nCorrelation Matrix:")
    print(correlation_matrix)
    
    import numpy as np

    # Define portfolio weights (50% each)
    weights = np.array([0.7, 0.3])


    # Portfolio daily returns
    portfolio_returns = returns.dot(weights)

    print("\nPortfolio Daily Returns:")
    print(portfolio_returns.head())

    # Portfolio annualized return
    portfolio_annual_return = portfolio_returns.mean() * 252

    print("\nPortfolio Annualized Return:")
    print(f"{portfolio_annual_return:.4f}")

    # Portfolio annualized volatility
    portfolio_annual_volatility = portfolio_returns.std() * np.sqrt(252)

    print("\nPortfolio Annualized Volatility:")
    print(f"{portfolio_annual_volatility:.4f}")

    # Individual stock annual volatility
    individual_volatility = returns.std() * np.sqrt(252)

    print("\nIndividual Stock Annualized Volatility:")
    print(individual_volatility)

    # Assume risk-free rate
    risk_free_rate = 0.04

    # Sharpe Ratio
    sharpe_ratio = (portfolio_annual_return - risk_free_rate) / portfolio_annual_volatility

    print("\nPortfolio Sharpe Ratio:")
    print(f"{sharpe_ratio:.4f}")

    print("\nTesting Different Weights:")

    best_sharpe = -999
    best_weights = None

    for w in np.linspace(0, 1, 101):
        weights = np.array([w, 1 - w])

        portfolio_returns = returns.dot(weights)
        portfolio_return = portfolio_returns.mean() * 252
        portfolio_vol = portfolio_returns.std() * np.sqrt(252)
        sharpe = (portfolio_return - risk_free_rate) / portfolio_vol

        if sharpe > best_sharpe:
            best_sharpe = sharpe
            best_weights = weights

    print("\nBest Portfolio Found:")
    print(f"Weights: AAPL={best_weights[0]:.2f}, MSFT={best_weights[1]:.2f}")
    print(f"Sharpe Ratio: {best_sharpe:.4f}")


# def main():
#     tickers = ["AAPL", "MSFT"]
#     start_date = "2020-01-01"
#     end_date = "2024-12-31"

#     # Load data
#     data = load_data(tickers, start_date, end_date)


#     # Calculate metrics
#     data = calculate_daily_returns(data)
#     data = data.dropna()

#     annual_volatility = calculate_annualized_volatility(data)

#     data = calculate_cumulative_return(data)
#     data = calculate_rolling_volatility(data)

#     max_drawdown = calculate_max_drawdown(data)

#     # Print key metrics
#     print(f"Annualized Volatility: {annual_volatility:.4f}")
#     print(f"Maximum Drawdown: {max_drawdown:.4f}")

#     #plot
#     plot_cumulative_return(data, ticker)


if __name__ == "__main__":
    main()
