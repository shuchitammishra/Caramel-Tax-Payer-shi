import numpy as np
import pandas as pd

def calculate_performance_stats(stock_prices, benchmark_prices, risk_free_rate=0.065):
    """
    Computes statistical comparison data between a stock and a benchmark.
    """
    df = pd.DataFrame({'Stock': stock_prices, 'Benchmark': benchmark_prices}).dropna()
    if len(df) < 15:
        return None

    stock_returns = df['Stock'].pct_change().dropna()
    bench_returns = df['Benchmark'].pct_change().dropna()
    returns_df = pd.DataFrame({'Stock': stock_returns, 'Benchmark': bench_returns}).dropna()

    # 1. Z-Score of the Spread (Stock Price / Benchmark Price ratio)
    spread = df['Stock'] / df['Benchmark']
    spread_mean = spread.mean()
    spread_std = spread.std()
    current_spread = spread.iloc[-1]
    z_score = (current_spread - spread_mean) / spread_std if spread_std > 0 else 0.0

    # 2. Total & Annualized Returns (CAGR)
    days = (df.index[-1] - df.index[0]).days
    years = days / 365.25 if days > 0 else 1.0
    
    stock_tot = (df['Stock'].iloc[-1] / df['Stock'].iloc[0]) - 1
    bench_tot = (df['Benchmark'].iloc[-1] / df['Benchmark'].iloc[0]) - 1
    
    stock_cagr = ((1 + stock_tot) ** (1 / years)) - 1
    bench_cagr = ((1 + bench_tot) ** (1 / years)) - 1

    # 3. Volatility & Sharpe Ratio
    stock_vol = stock_returns.std() * np.sqrt(252)
    bench_vol = bench_returns.std() * np.sqrt(252)
    
    stock_sharpe = (stock_cagr - risk_free_rate) / stock_vol if stock_vol > 0 else 0.0
    bench_sharpe = (bench_cagr - risk_free_rate) / bench_vol if bench_vol > 0 else 0.0

    # 4. Beta & Alpha (CAPM)
    cov = np.cov(returns_df['Stock'], returns_df['Benchmark'])[0][1]
    bench_var = np.var(returns_df['Benchmark'])
    beta = cov / bench_var if bench_var > 0 else 1.0
    alpha = stock_cagr - (risk_free_rate + beta * (bench_cagr - risk_free_rate))

    # 5. Correlation & Max Drawdown
    correlation = returns_df['Stock'].corr(returns_df['Benchmark'])

    def max_drawdown(series):
        roll_max = series.cummax()
        return ((series - roll_max) / roll_max).min()

    stock_mdd = max_drawdown(df['Stock'])
    bench_mdd = max_drawdown(df['Benchmark'])

    return {
        "Z-Score (Relative Valuation Spread)": round(z_score, 2),
        "Stock Total Return (%)": round(stock_tot * 100, 2),
        "Benchmark Total Return (%)": round(bench_tot * 100, 2),
        "Stock CAGR (%)": round(stock_cagr * 100, 2),
        "Benchmark CAGR (%)": round(bench_cagr * 100, 2),
        "Stock Volatility (%)": round(stock_vol * 100, 2),
        "Benchmark Volatility (%)": round(bench_vol * 100, 2),
        "Stock Sharpe Ratio": round(stock_sharpe, 2),
        "Benchmark Sharpe Ratio": round(bench_sharpe, 2),
        "Beta": round(beta, 2),
        "Alpha (%)": round(alpha * 100, 2),
        "Correlation": round(correlation, 2),
        "Stock Max Drawdown (%)": round(stock_mdd * 100, 2),
        "Benchmark Max Drawdown (%)": round(bench_mdd * 100, 2)
    }