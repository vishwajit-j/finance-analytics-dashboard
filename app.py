from data_loader import load_data
from metrics import (
    calculate_daily_returns,
    calculate_correlation_matrix,
)
from portfolio import optimize_portfolio
from portfolio import walk_forward_optimization
from plots import plot_efficient_frontier
import numpy as np
import matplotlib.pyplot as plt
from metrics import calculate_portfolio_drawdown
from metrics import calculate_var, calculate_cvar
from metrics import calculate_calmar_ratio
from metrics import calculate_rolling_sharpe
from plots import plot_rolling_metric
from metrics import generate_portfolio_summary
from metrics import calculate_sharpe, calculate_sortino
from metrics import train_test_split_returns



def main():

    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "SPY"]
    start_date = "2020-01-01"
    end_date = "2024-12-31"
    risk_free_rate = 0.04

    # ----------------------------
    # Load Data
    # ----------------------------
    data = load_data(tickers, start_date, end_date)
    returns = calculate_daily_returns(data)

    # Separate benchmark (SPY)
    benchmark_returns = returns["SPY"]
    asset_returns = returns.drop(columns=["SPY"])

    # ----------------------------
    # Train-Test Split
    # ----------------------------
    split_date = "2023-01-01"

    train_assets = asset_returns[asset_returns.index < split_date]
    test_assets = asset_returns[asset_returns.index >= split_date]

    train_benchmark = benchmark_returns[benchmark_returns.index < split_date]
    test_benchmark = benchmark_returns[benchmark_returns.index >= split_date]

    print("\nTrain Period:", train_assets.index.min(), "to", train_assets.index.max())
    print("Test Period:", test_assets.index.min(), "to", test_assets.index.max())

    # ----------------------------
    # Portfolio Optimization (TRAIN ONLY)
    # ----------------------------
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
        train_assets,
        risk_free_rate=risk_free_rate,
        simulations=5000
    )

    # ----------------------------
    # Print Optimized Weights
    # ----------------------------
    print("\nOptimized Portfolio (TRAIN DATA):")

    for ticker, weight in zip(train_assets.columns, best_weights):
        print(f"{ticker}: {weight:.4f}")
    print(f"Train Sharpe Ratio: {best_sharpe:.4f}")

    # ----------------------------
    # OUT-OF-SAMPLE Evaluation
    # ----------------------------
    best_portfolio_returns = test_assets.dot(best_weights)
    min_portfolio_returns = test_assets.dot(min_vol_weights)
    max_portfolio_returns = test_assets.dot(max_return_weights)

    # Annual Metrics (OOS)
    best_return = best_portfolio_returns.mean() * 252
    best_vol = best_portfolio_returns.std() * np.sqrt(252)

    min_return_oos = min_portfolio_returns.mean() * 252
    min_vol_oos = min_portfolio_returns.std() * np.sqrt(252)

    max_return_oos = max_portfolio_returns.mean() * 252
    max_vol_oos = max_portfolio_returns.std() * np.sqrt(252)

    # Risk Metrics (OOS)
    best_drawdown = calculate_portfolio_drawdown(best_portfolio_returns)
    min_drawdown = calculate_portfolio_drawdown(min_portfolio_returns)
    max_drawdown = calculate_portfolio_drawdown(max_portfolio_returns)

    best_sharpe_calc = calculate_sharpe(best_portfolio_returns, risk_free_rate)
    min_sharpe_calc = calculate_sharpe(min_portfolio_returns, risk_free_rate)
    max_sharpe_calc = calculate_sharpe(max_portfolio_returns, risk_free_rate)

    best_sortino_calc = calculate_sortino(best_portfolio_returns, risk_free_rate)
    min_sortino_calc = calculate_sortino(min_portfolio_returns, risk_free_rate)
    max_sortino_calc = calculate_sortino(max_portfolio_returns, risk_free_rate)

    best_calmar = calculate_calmar_ratio(best_return, best_drawdown)
    min_calmar = calculate_calmar_ratio(min_return_oos, min_drawdown)
    max_calmar = calculate_calmar_ratio(max_return_oos, max_drawdown)

    # ----------------------------
    # Portfolio Summary (OOS ONLY)
    # ----------------------------
    portfolio_summary_data = {
        "Max Sharpe": {
            "Return": best_return,
            "Volatility": best_vol,
            "Sharpe": best_sharpe_calc,
            "Sortino": best_sortino_calc,
            "Max Drawdown": best_drawdown,
            "Calmar": best_calmar,
            "VaR (95%)": calculate_var(best_portfolio_returns),
            "CVaR (95%)": calculate_cvar(best_portfolio_returns)
        },
        "Min Volatility": {
            "Return": min_return_oos,
            "Volatility": min_vol_oos,
            "Sharpe": min_sharpe_calc,
            "Sortino": min_sortino_calc,
            "Max Drawdown": min_drawdown,
            "Calmar": min_calmar,
            "VaR (95%)": calculate_var(min_portfolio_returns),
            "CVaR (95%)": calculate_cvar(min_portfolio_returns)
        },
        "Max Return": {
            "Return": max_return_oos,
            "Volatility": max_vol_oos,
            "Sharpe": max_sharpe_calc,
            "Sortino": max_sortino_calc,
            "Max Drawdown": max_drawdown,
            "Calmar": max_calmar,
            "VaR (95%)": calculate_var(max_portfolio_returns),
            "CVaR (95%)": calculate_cvar(max_portfolio_returns)
        }
    }

    summary_df = generate_portfolio_summary(portfolio_summary_data)

    print("\n================ OOS Portfolio Comparison ================\n")
    print(summary_df.round(4))

    # ----------------------------
    # Walk Forward Optimization
    # ----------------------------
    wf_returns = walk_forward_optimization(
        asset_returns,   # IMPORTANT: not including SPY
        train_years=2,
        test_months=6,
        risk_free_rate=risk_free_rate
    )

    if wf_returns is not None:

        wf_annual_return = wf_returns.mean() * 252
        wf_vol = wf_returns.std() * np.sqrt(252)
        wf_sharpe = calculate_sharpe(wf_returns, risk_free_rate)
        wf_drawdown = calculate_portfolio_drawdown(wf_returns)

        print("\n================ Walk Forward Results ================")
        print(f"Annual Return: {wf_annual_return:.4f}")
        print(f"Volatility: {wf_vol:.4f}")
        print(f"Sharpe Ratio: {wf_sharpe:.4f}")
        print(f"Max Drawdown: {wf_drawdown:.4f}")

        wf_cumulative = (1 + wf_returns).cumprod()

        plt.figure(figsize=(10,5))
        plt.plot(wf_cumulative)
        plt.title("Walk Forward Strategy Growth")
        plt.xlabel("Date")
        plt.ylabel("Growth of $1")
        plt.show()

    # ----------------------------
    # Rolling Sharpe (OOS)
    # ----------------------------
    rolling_sharpe_best = calculate_rolling_sharpe(best_portfolio_returns, risk_free_rate)
    rolling_sharpe_min = calculate_rolling_sharpe(min_portfolio_returns, risk_free_rate)
    rolling_sharpe_max = calculate_rolling_sharpe(max_portfolio_returns, risk_free_rate)

    plot_rolling_metric(
        {
            "Max Sharpe": rolling_sharpe_best,
            "Min Volatility": rolling_sharpe_min,
            "Max Return": rolling_sharpe_max,
        },
        title="Rolling Sharpe Ratio (OOS)"
    )

    # ----------------------------
    # Efficient Frontier (TRAIN)
    # ----------------------------
    plot_efficient_frontier(
        all_volatilities,
        all_returns,
        all_sharpes,
        train_assets.dot(best_weights).std() * np.sqrt(252),
        train_assets.dot(best_weights).mean() * 252,
        best_sharpe,
        min_volatility,
        min_return,
        max_vol,
        max_return,
        risk_free_rate
    )



if __name__ == "__main__":
    main()
