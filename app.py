import yfinance as yf
import pandas as pd

# Choose a stock
ticker = "AAPL"

# Download historical data
data = yf.download(ticker, start="2020-01-01", end="2024-12-31")

# Display first few rows
print(data.head())

# Display basic info
print("\nData Info:")
print(data.info())

# Flatten columns if multi-index
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

print("\nCleaned Columns:")
print(data.columns)

# Calculate Daily Returns
data["Daily Return"] = data["Close"].pct_change()

print("\nDaily Return:")
print(data[["Close", "Daily Return"]].head())

# Drop NaN values
data = data.dropna()

print("\nAfter Dropping NaN:")
print(data.head())

# Calculate Daily Volatility (Standard Deviation of Returns)
daily_volatility = data["Daily Return"].std()

print("\nDaily Volatility:")
print(daily_volatility)

import numpy as np

annual_volatility = daily_volatility * np.sqrt(252)

print("\nAnnualized Volatility:")
print(annual_volatility)

# Cumulative Return
data["Cumulative Return"] = (1 + data["Daily Return"]).cumprod()

print("\nCumulative Returns:")
print(data[["Daily Return", "Cumulative Return"]].head())

# 20-Day Rolling Volatility
data["Rolling Volatility (20d)"] = (
    data["Daily Return"]
    .rolling(window=20)
    .std()
    * np.sqrt(252)
)

print("\nRolling Volatility:")
print(data[["Daily Return", "Rolling Volatility (20d)"]].head(25))

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.plot(data.index, data["Cumulative Return"])
plt.title("Cumulative Return Over Time")
plt.xlabel("Date")
plt.ylabel("Growth of $1")
plt.show()

# Maximum Drawdown

rolling_max = data["Cumulative Return"].cummax()
drawdown = data["Cumulative Return"] / rolling_max - 1
max_drawdown = drawdown.min()

print("\nMaximum Drawdown:")
print(max_drawdown)
