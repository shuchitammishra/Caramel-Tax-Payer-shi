import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def plot_backtest(stock_symbol, benchmark_symbol, period="1y"):
    data = yf.download([stock_symbol, benchmark_symbol], period=period, progress=False)['Close']
    if data.empty or isinstance(data, pd.Series) or stock_symbol not in data.columns or benchmark_symbol not in data.columns:
        print("❌ Error fetching price data for comparison.")
        return None, None

    data = data.dropna()
    stock_prices = data[stock_symbol]
    bench_prices = data[benchmark_symbol]

    norm_stock = (stock_prices / stock_prices.iloc[0]) * 100
    norm_bench = (bench_prices / bench_prices.iloc[0]) * 100

    plt.figure(figsize=(12, 6))
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    plt.plot(norm_stock.index, norm_stock, label=f'Stock: {stock_symbol}', linewidth=2)
    plt.plot(norm_bench.index, norm_bench, label=f'Benchmark: {benchmark_symbol}', linestyle='--', color='black', linewidth=2)

    plt.title(f'Performance Comparison: {stock_symbol} vs {benchmark_symbol} ({period.upper()})', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=11)
    plt.ylabel('Normalized Growth (Base = 100)', fontsize=11)
    plt.axhline(100, color='gray', linestyle=':', alpha=0.7)
    plt.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    plt.show()

    return stock_prices, bench_prices