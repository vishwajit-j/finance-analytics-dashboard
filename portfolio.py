import numpy as np

def optimize_portfolio(returns, risk_free_rate=0.04, simulations=5000):

    num_assets = returns.shape[1]

    best_sharpe = -999
    best_weights = None

    all_returns = []
    all_volatilities = []
    all_sharpes = []

    for _ in range(simulations):

        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)

        portfolio_returns = returns.dot(weights)

        annual_return = portfolio_returns.mean() * 252
        annual_volatility = portfolio_returns.std() * np.sqrt(252)

        sharpe = (annual_return - risk_free_rate) / annual_volatility

        all_returns.append(annual_return)
        all_volatilities.append(annual_volatility)
        all_sharpes.append(sharpe)

        if sharpe > best_sharpe:
            best_sharpe = sharpe
            best_weights = weights

    return (
        best_weights,
        best_sharpe,
        all_returns,
        all_volatilities,
        all_sharpes
    )
