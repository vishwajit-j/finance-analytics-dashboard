import yfinance as yf
import pandas as pd


def load_data(tickers, start, end):
    """
    Load stock data for one or multiple tickers.
    """

    data = yf.download(tickers, start=start, end=end)

    # If only one ticker, flatten columns
    if isinstance(tickers, str):
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

    return data
