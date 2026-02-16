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


def calculate_portfolio_drawdown(portfolio_returns):

    cumulative = (1 + portfolio_returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = cumulative / rolling_max - 1

    max_drawdown = drawdown.min()

    return max_drawdown



def calculate_sortino_ratio(portfolio_returns, risk_free_rate=0.04):
    import numpy as np
    
    annual_return = portfolio_returns.mean() * 252
    
    downside_returns = portfolio_returns[portfolio_returns < 0]
    downside_volatility = downside_returns.std() * np.sqrt(252)
    
    sortino = (annual_return - risk_free_rate) / downside_volatility
    
    return sortino
