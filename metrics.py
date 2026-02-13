import numpy as np


def calculate_daily_returns(data):
    data["Daily Return"] = data["Close"].pct_change()
    return data


def calculate_annualized_volatility(data):
    daily_volatility = data["Daily Return"].std()
    annual_volatility = daily_volatility * np.sqrt(252)
    return annual_volatility


def calculate_cumulative_return(data):
    data["Cumulative Return"] = (1 + data["Daily Return"]).cumprod()
    return data


def calculate_rolling_volatility(data, window=20):
    data["Rolling Volatility"] = (
        data["Daily Return"]
        .rolling(window=window)
        .std()
        * np.sqrt(252)
    )
    return data


def calculate_max_drawdown(data):
    rolling_max = data["Cumulative Return"].cummax()
    drawdown = data["Cumulative Return"] / rolling_max - 1
    max_drawdown = drawdown.min()
    return max_drawdown
