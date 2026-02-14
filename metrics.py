import numpy as np


def calculate_daily_returns(data):
    close_prices = data["Close"]
    return close_prices.pct_change().dropna()




def calculate_annualized_volatility(returns, periods=252):
    return returns.std() * np.sqrt(periods)



def calculate_cumulative_return(returns):
    return (1 + returns).cumprod()


def calculate_rolling_volatility(returns, window=20, periods=252):
    return returns.rolling(window=window).std() * np.sqrt(periods)



def calculate_max_drawdown(cumulative_returns):
    rolling_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / rolling_max - 1
    return drawdown.min()


def calculate_correlation_matrix(returns):
    return returns.corr()
