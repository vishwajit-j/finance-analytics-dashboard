import matplotlib.pyplot as plt


def plot_cumulative_return(data, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["Cumulative Return"])
    plt.title(f"Cumulative Return of {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.show()


def plot_efficient_frontier(volatilities, returns, sharpes, best_vol, best_return):
    plt.figure(figsize=(10, 6))

    scatter = plt.scatter(
        volatilities,
        returns,
        c=sharpes,
        cmap="viridis",
        alpha=0.6
    )

    plt.colorbar(scatter, label="Sharpe Ratio")

    # Mark optimal portfolio
    plt.scatter(best_vol, best_return, color="red", marker="*", s=300)

    plt.xlabel("Volatility (Risk)")
    plt.ylabel("Expected Return")
    plt.title("Efficient Frontier (Monte Carlo Simulation)")

    plt.show()