import numpy as np

def optimize_portfolio(
    returns,
    risk_free_rate=0.04,
    simulations=5000,
    max_weight=1.0
):

    num_assets = returns.shape[1]

    best_sharpe = -999
    best_weights = None

    best_sortino = -999
    best_sortino_weights = None

    min_volatility = float("inf")
    min_vol_weights = None

    max_return = -float("inf")
    max_return_weights = None


    all_returns = []
    all_volatilities = []
    all_sharpes = []

    min_volatility = float("inf")
    min_vol_weights = None
    min_return = None

    max_return = -float("inf")
    max_return_weights = None
    max_vol = None

    #Monte Carlo loop
    for _ in range(simulations):

        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)

        # Enforce max weight constraint
        if np.any(weights > max_weight):
            continue

        portfolio_returns = returns.dot(weights)

        annual_return = portfolio_returns.mean() * 252
        annual_volatility = portfolio_returns.std() * np.sqrt(252)

        sharpe = (annual_return - risk_free_rate) / annual_volatility

        # Downside deviation (only negative returns)
        downside_returns = portfolio_returns[portfolio_returns < 0]
        downside_std = downside_returns.std() * np.sqrt(252)

        if downside_std != 0:
            sortino = (annual_return - risk_free_rate) / downside_std
        else:
            sortino = 0

        if sortino > best_sortino:
            best_sortino = sortino
            best_sortino_weights = weights



        if annual_volatility < min_volatility:
            min_volatility = annual_volatility
            min_vol_weights = weights
            min_return = annual_return


        if annual_return > max_return:
            max_return = annual_return
            max_return_weights = weights
            max_vol = annual_volatility



        all_returns.append(annual_return)
        all_volatilities.append(annual_volatility)
        all_sharpes.append(sharpe)

        if sharpe > best_sharpe:
            best_sharpe = sharpe
            best_weights = weights



    return (
    best_weights,
    best_sharpe,
    min_vol_weights,
    min_volatility,
    min_return,
    max_return_weights,
    max_return,
    max_vol,
    best_sortino_weights,
    best_sortino,
    all_returns,
    all_volatilities,
    all_sharpes
)



def walk_forward_optimization(returns, train_years=2, test_months=6, risk_free_rate=0.04):

    import pandas as pd

    walk_forward_returns = []

    start_date = returns.index.min()
    end_date = returns.index.max()

    current_start = start_date

    while True:

        train_end = current_start + pd.DateOffset(years=train_years)
        test_end = train_end + pd.DateOffset(months=test_months)

        if test_end > end_date:
            break

        train_data = returns[(returns.index >= current_start) & (returns.index < train_end)]
        test_data = returns[(returns.index >= train_end) & (returns.index < test_end)]

        if len(train_data) == 0 or len(test_data) == 0:
            break

        (
            best_weights,
            _,
            _,
            _,
            _,
            _,
            _,
            _,
            _,
            _,
            _,
            _,
            _
        ) = optimize_portfolio(
            train_data,
            risk_free_rate=risk_free_rate,
            simulations=3000,
            max_weight=0.25
        )

        test_portfolio_returns = test_data.dot(best_weights)

        walk_forward_returns.append(test_portfolio_returns)

        current_start = current_start + pd.DateOffset(months=test_months)

    if len(walk_forward_returns) == 0:
        return None

    return pd.concat(walk_forward_returns)

