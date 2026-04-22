import numpy as np
import pandas as pd

def calculate_daily_returns(data):
    close_prices = data["Close"]
    return close_prices.pct_change(fill_method=None).dropna()




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

def calculate_sharpe(returns, risk_free_rate):
    annual_return = returns.mean() * 252
    annual_vol = returns.std() * np.sqrt(252)
    return (annual_return - risk_free_rate) / annual_vol


def calculate_calmar_ratio(annual_return, max_drawdown):
    """
    Calmar Ratio = Annual Return / |Max Drawdown|
    """
    if max_drawdown == 0:
        return 0  # avoid division error
    
    return annual_return / abs(max_drawdown)


def calculate_sortino(portfolio_returns, risk_free_rate):
    
    annual_return = portfolio_returns.mean() * 252
    
    downside_returns = portfolio_returns[portfolio_returns < 0]
    downside_volatility = downside_returns.std() * np.sqrt(252)
    
    sortino = (annual_return - risk_free_rate) / downside_volatility
    
    return sortino


def calculate_var(portfolio_returns, confidence=0.95):
    """
    Historical Value at Risk (VaR)
    """
    sorted_returns = np.sort(portfolio_returns)
    index = int((1 - confidence) * len(sorted_returns))
    return sorted_returns[index]


def calculate_cvar(portfolio_returns, confidence=0.95):
    """
    Historical Conditional Value at Risk (CVaR)
    """
    sorted_returns = np.sort(portfolio_returns)
    index = int((1 - confidence) * len(sorted_returns))
    return sorted_returns[:index].mean()


def calculate_rolling_sharpe(portfolio_returns, risk_free_rate=0.04, window=126):
    """
    Rolling Sharpe Ratio
    window=126 ≈ 6 months of trading days
    """

    excess_returns = portfolio_returns - risk_free_rate / 252

    rolling_mean = excess_returns.rolling(window=window).mean()
    rolling_std = excess_returns.rolling(window=window).std()

    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

    return rolling_sharpe



def generate_portfolio_summary(returns):
    import numpy as np

    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]

    annual_return = returns.mean() * 252
    volatility = returns.std() * np.sqrt(252)
    sharpe = annual_return / volatility if volatility != 0 else 0

    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    return {
        "Return": annual_return,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "Max Drawdown": max_drawdown
    }

def train_test_split_returns(returns, split_date):
    """
    Split returns into train and test sets based on split_date.
    """

    train_returns = returns[returns.index < split_date]
    test_returns = returns[returns.index >= split_date]

    return train_returns, test_returns


def calculate_beta(strategy_returns, benchmark_returns):
    covariance = np.cov(strategy_returns, benchmark_returns)[0][1]
    benchmark_variance = np.var(benchmark_returns)
    return covariance / benchmark_variance


def calculate_alpha(strategy_returns, benchmark_returns, risk_free_rate):
    beta = calculate_beta(strategy_returns, benchmark_returns)

    strategy_annual = strategy_returns.mean() * 252
    benchmark_annual = benchmark_returns.mean() * 252

    alpha = strategy_annual - (
        risk_free_rate + beta * (benchmark_annual - risk_free_rate)
    )

    return alpha


def calculate_information_ratio(strategy_returns, benchmark_returns):
    active_returns = strategy_returns - benchmark_returns
    tracking_error = active_returns.std() * np.sqrt(252)

    if tracking_error == 0:
        return 0

    return (active_returns.mean() * 252) / tracking_error

def capm_regression(strategy_returns, benchmark_returns):
    import statsmodels.api as sm

    X = sm.add_constant(benchmark_returns)  # adds intercept
    y = strategy_returns

    model = sm.OLS(y, X).fit()

    return model


def calculate_risk_contribution(weights, covariance_matrix):
    """
    Computes asset-level contribution to total portfolio volatility.

    Returns:
    - risk_contribution (absolute contribution)
    - percentage_contribution (% of total portfolio volatility)
    """

    # Portfolio volatility
    portfolio_vol = np.sqrt(weights.T @ covariance_matrix @ weights)

    # Marginal contribution
    marginal_contribution = covariance_matrix @ weights / portfolio_vol

    # Total contribution
    risk_contribution = weights * marginal_contribution

    # Percentage contribution
    percentage_contribution = risk_contribution / portfolio_vol

    return risk_contribution, percentage_contribution
            

def calculate_rolling_beta(strategy_returns, benchmark_returns, window=126):
    """
    Rolling Beta (time-varying market exposure)
    """

    rolling_cov = strategy_returns.rolling(window).cov(benchmark_returns)
    rolling_var = benchmark_returns.rolling(window).var()

    rolling_beta = rolling_cov / rolling_var

    return rolling_beta