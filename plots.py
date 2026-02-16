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
    min_vol,
    min_return,
    max_vol,
    max_return
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

    plt.show()
