# 📈 Indian Stock Backtester & Statistical Comparator

A powerful Python tool designed to scan the **National Stock Exchange of India (NSE)** for fundamentally undervalued companies, backtest their historical price performance against major benchmark indices or ETFs, and generate deep quantitative statistical analytics (including Spread Z-Score, Sharpe Ratio, Beta, Alpha, and Maximum Drawdown).

---

## ✨ Features

- **Automated Market Screening:** Dynamically downloads the live NSE equity registry and filters for value stocks using fundamental metrics (Price-to-Earnings, Price-to-Book, Debt-to-Equity, and Return on Equity).
- **Flexible Benchmarking:** Compare screened stocks or custom tickers directly against major Indian market indices (`NIFTY 50`, `NIFTY 500`, `NIFTY Bank`, `NIFTY IT`) or ETFs (`NIFTYBEES.NS`, `BANKBEES.NS`).
- **Normalized Growth Visualizer:** Plots clean, normalized comparative performance charts (Base = 100) using `matplotlib`.
- **Comprehensive Statistical Suite:** Computes institutional-grade metrics to evaluate risk-adjusted returns:
  - **Z-Score of the Spread:** Measures historical valuation divergence to spot statistical undervaluation.
  - **Sharpe Ratio:** Evaluates risk-adjusted performance relative to a risk-free rate.
  - **Beta & Alpha:** Measures stock volatility and excess returns relative to the benchmark index (CAPM model).
  - **Max Drawdown:** Calculates peak-to-trough historical losses.

---

## 📁 Project File Structure

```text
indian_stock_backtester/
├── requirements.txt         # Python dependencies
├── config.py                # Benchmark options & screening thresholds
├── screener.py              # NSE market downloader & fundamental filter engine
├── stats_calculator.py      # Quantitative analytics (Z-Score, Sharpe, Beta, Alpha)
├── visualizer.py            # Comparative charting engine
├── main.py                  # Interactive CLI application menu
└── .gitignore               # Git exclusion rules
