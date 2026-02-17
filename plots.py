import matplotlib.pyplot as plt


def plot_cumulative_return(data, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["Cumulative Return"])
    plt.title(f"Cumulative Return of {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.show()

def plot_efficient_frontier(
    volatilities,
    returns,
    sharpes,
    best_vol,
    best_return,
    best_sharpe,
    min_vol,
    min_return,
    max_vol,
    max_return,
    risk_free_rate
):
    plt.figure(figsize=(10, 6))

    scatter = plt.scatter(
        volatilities,
        returns,
        c=sharpes,
        cmap="viridis",
        alpha=0.6
    )

    plt.colorbar(scatter, label="Sharpe Ratio")

    # Max Sharpe Portfolio
    plt.scatter(best_vol, best_return, color="red", marker="*", s=300, label="Max Sharpe")

    # Minimum Volatility Portfolio
    plt.scatter(min_vol, min_return, color="blue", marker="o", s=150, label="Min Volatility")

    # Maximum Return Portfolio
    plt.scatter(max_vol, max_return, color="green", marker="^", s=150, label="Max Return")

    plt.xlabel("Volatility (Risk)")
    plt.ylabel("Expected Return")
    plt.title("Efficient Frontier (Monte Carlo Simulation)")
    plt.legend()

    import numpy as np

    # Capital Allocation Line (CAL)
    risk_free_rate = 0.04  # must match optimizer input

    vol_range = np.linspace(0, max(volatilities), 100)

    cal_returns = risk_free_rate + best_sharpe * vol_range

    plt.plot(vol_range, cal_returns, color="black", linestyle="--", label="Capital Allocation Line")

    plt.show()

def plot_rolling_metric(metric_series_dict, title):
    plt.figure(figsize=(12, 6))

    for label, series in metric_series_dict.items():
        plt.plot(series.index, series, label=label)

    plt.axhline(0, linestyle="--", color="black", alpha=0.5)

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.show()
