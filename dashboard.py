import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from datetime import datetime, timedelta

from data_loader import load_data
from metrics import calculate_daily_returns, calculate_risk_contribution
from portfolio import optimize_portfolio, risk_parity_weights
from plots import plot_risk_contribution, plot_efficient_frontier

# ================= CONFIG =================
st.set_page_config(page_title="Portfolio Analytics", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Portfolio Analytics Dashboard")

# ================= HELP =================
with st.expander("📘 How to Use This Dashboard"):
    st.markdown("""
This tool helps analyze portfolio performance, risk, and optimization.

**Steps:**
1. Select assets  
2. Choose strategy  
3. Adjust date range  

**What you’ll see:**
- Performance → How your investment grows  
- Risk → Where risk comes from  
- Optimization → Best risk-return combinations  
""")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Controls")

tickers = st.sidebar.multiselect(
    "Assets",
    ["AAPL", "AMZN", "BTC-USD", "EEM", "GLD", "GOOGL", "MSFT", "TLT", "XLE"],
    default=["AAPL", "MSFT", "GLD", "BTC-USD", "TLT"]
)

strategy = st.sidebar.radio(
    "Strategy",
    ["Max Sharpe", "Risk Parity"]
)

today = datetime.today()
default_start = today - timedelta(days=5*365)

start = st.sidebar.date_input("Start Date", value=default_start)
end = st.sidebar.date_input("End Date", value=today)

st.sidebar.markdown("---")
st.sidebar.info("""
💡 Tips:
- Use 3–6 assets for balance  
- Longer periods give more stable results  
- Compare strategies for insights  
""")

# ================= VALIDATION =================
if len(tickers) < 2:
    st.warning("Please select at least 2 assets")
    st.stop()

start = pd.to_datetime(start)
end = pd.to_datetime(end)

if start >= end:
    st.error("Start date must be before end date")
    st.stop()

# ================= DATA =================
prices = load_data(tickers, start, end)

if prices is None or prices.empty:
    st.error("No data available for selected inputs")
    st.stop()

returns = calculate_daily_returns(prices)

split = int(len(returns) * 0.7)
train = returns.iloc[:split]
test = returns.iloc[split:]

if train.empty or test.empty:
    st.error("Not enough data — try longer date range")
    st.stop()

# ================= STRATEGY =================
if strategy == "Max Sharpe":
    (
        weights,
        sharpe,
        min_vol_weights,
        min_vol,
        min_return,
        max_return_weights,
        max_return,
        max_vol,
        _,
        _,
        all_returns,
        all_vols,
        all_sharpes
    ) = optimize_portfolio(train)

else:
    cov = train.cov() * 252
    weights = risk_parity_weights(cov)

    port = train.dot(weights)
    sharpe = np.mean(port) * 252 / (np.std(port) * np.sqrt(252))

    all_returns, all_vols, all_sharpes = [], [], []

# ================= KPI =================
st.subheader("📊 Portfolio Summary")

def sharpe_comment(x):
    if x > 1.5:
        return "Excellent"
    elif x > 1:
        return "Good"
    elif x > 0.5:
        return "Moderate"
    else:
        return "Weak"

col1, col2, col3 = st.columns(3)

col1.metric("Sharpe Ratio", f"{sharpe:.2f}")
col1.caption(f"{sharpe_comment(sharpe)} risk-adjusted performance")

col2.metric("Assets", len(tickers))
col2.caption("Diversification level")

col3.metric("Strategy", strategy)

st.divider()

# ================= TABS =================
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Performance",
    "Risk",
    "Optimization"
])

# ================= OVERVIEW =================
with tab1:
    st.subheader("Portfolio Allocation")

    weights_df = pd.DataFrame({
        "Asset": train.columns,
        "Weight": weights
    }).sort_values(by="Weight", ascending=False)

    st.dataframe(weights_df, use_container_width=True)
    st.bar_chart(weights_df.set_index("Asset"))

    st.caption("Shows how capital is distributed across assets")

# ================= PERFORMANCE =================
with tab2:
    st.subheader("Portfolio Growth")

    portfolio_returns = test.dot(weights)
    cum = (1 + portfolio_returns).cumprod()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=cum.index,
        y=cum,
        mode='lines',
        name='Portfolio'
    ))

    fig.update_layout(
        title="Growth of $1 Invested",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("Tracks how $1 invested grows over time")

    # Drawdown
    st.subheader("Drawdown")

    peak = cum.cummax()
    drawdown = (cum - peak) / peak
    max_dd = drawdown.min()

    fig_dd = go.Figure()
    fig_dd.add_trace(go.Scatter(
        x=drawdown.index,
        y=drawdown,
        mode='lines',
        name='Drawdown',
        line=dict(color='red')
    ))

    fig_dd.update_layout(
        title="Loss from Previous Peak",
        xaxis_title="Date",
        yaxis_title="Drawdown",
        template="plotly_dark"
    )

    st.plotly_chart(fig_dd, use_container_width=True)

    st.error(f"Max Drawdown: {max_dd:.2%}")

# ================= RISK =================
with tab3:
    st.subheader("Risk Contribution")

    cov = train.cov() * 252
    rc, rc_pct = calculate_risk_contribution(weights, cov)

    fig1 = plot_risk_contribution(train.columns, rc_pct * 100)
    st.pyplot(fig1, width="stretch")

    top_asset = train.columns[np.argmax(rc_pct)]

    st.info(f"""
Top risk contributor: **{top_asset}**

This asset has the largest impact on portfolio volatility.
""")

    # Correlation
    st.subheader("Correlation Between Assets")

    corr = train.corr()

    fig_corr = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1
    ))

    fig_corr.update_layout(template="plotly_dark")

    st.plotly_chart(fig_corr, use_container_width=True)

# ================= OPTIMIZATION =================
with tab4:
    if strategy == "Max Sharpe":

        st.subheader("Efficient Frontier")

        best_vol = np.std(train.dot(weights)) * np.sqrt(252)
        best_ret = np.mean(train.dot(weights)) * 252

        fig2 = plot_efficient_frontier(
            all_vols,
            all_returns,
            all_sharpes,
            best_vol,
            best_ret,
            sharpe,
            min_vol,
            min_return,
            max_vol,
            max_return,
            0.04
        )

        st.pyplot(fig2, width="stretch")

        st.caption("Shows trade-off between risk and return")

    else:
        st.info("Efficient frontier available only for Max Sharpe strategy")