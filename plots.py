import matplotlib.pyplot as plt


def plot_cumulative_return(data, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["Cumulative Return"])
    plt.title(f"Cumulative Return of {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.show()
