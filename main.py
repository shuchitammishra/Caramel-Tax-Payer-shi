import sys
from config import POPULAR_BENCHMARKS, SCREENING_CRITERIA, DEFAULT_PERIOD
from screener import fetch_nse_tickers, scan_undervalued_stocks
from visualizer import plot_backtest
from stats_calculator import calculate_performance_stats

def select_benchmark():
    print("\n--- SELECT BENCHMARK / INDEX FUND ---")
    for key, val in POPULAR_BENCHMARKS.items():
        print(f"[{key}] {val['name']}")
    print("[0] Enter custom ticker symbol (e.g., NIFTYBEES.NS, ^NSEI)")
    
    choice = input("\nEnter your choice (0-6): ").strip()
    if choice in POPULAR_BENCHMARKS:
        return POPULAR_BENCHMARKS[choice]['symbol']
    elif choice == '0':
        custom = input("Enter custom ticker symbol (include .NS if applicable): ").strip()
        return custom
    else:
        print("⚠️ Invalid choice. Defaulting to NIFTY 50 (^NSEI).")
        return "^NSEI"

def main():
    print("==========================================================")
    print("  INDIAN STOCK BACKTESTER & STATISTICAL COMPARATOR")
    print("==========================================================")

    while True:
        print("\n--- MAIN MENU ---")
        print("[1] Run Automated Value Screener & Backtest a Match")
        print("[2] Backtest a Custom Stock Symbol Directly")
        print("[3] Exit")
        
        mode = input("\nSelect mode (1-3): ").strip()
        
        if mode == '3':
            print("Exiting program. Happy investing!")
            sys.exit(0)
            
        benchmark = select_benchmark()
        period = input(f"Enter backtest time period [6m, 1y, 2y, 5y] (default '{DEFAULT_PERIOD}'): ").strip()
        if not period:
            period = DEFAULT_PERIOD

        stock_symbol = ""
        
        if mode == '1':
            limit_input = input("Enter max stocks to scan for testing (e.g., 100, or leave blank for full scan): ").strip()
            limit = int(limit_input) if limit_input.isdigit() else 100
            
            all_tickers = fetch_nse_tickers()
            df_screener = scan_undervalued_stocks(all_tickers, SCREENING_CRITERIA, limit=limit)
            
            if df_screener.empty:
                print("❌ No stocks matched your screening filters.")
                continue
                
            print("\n--- SCREENING RESULTS ---")
            print(df_screener.to_string(index=False))
            
            stock_symbol = input("\nEnter the Ticker symbol from the list above to backtest (e.g. INFY.NS): ").strip().upper()
            if not stock_symbol:
                continue
                
        elif mode == '2':
            stock_symbol = input("Enter stock symbol to backtest (e.g., RELIANCE.NS, TATAMOTORS.NS): ").strip().upper()
        
        if not stock_symbol:
            print("❌ Invalid stock symbol.")
            continue

        print(f"\n🚀 Running backtest for {stock_symbol} vs {benchmark} over {period.upper()}...")
        
        # Step 1: Plot chart
        stock_prices, bench_prices = plot_backtest(stock_symbol, benchmark, period=period)
        
        if stock_prices is not None and bench_prices is not None:
            # Step 2: Compute Statistics
            stats = calculate_performance_stats(stock_prices, bench_prices)
            
            if stats:
                print(f"\n================ STATISTICAL COMPARISON REPORT ================")
                print(f" Comparison: {stock_symbol} vs {benchmark}")
                print(f"----------------------------------------------------------------")
                for key, val in stats.items():
                    print(f" • {key:<35}: {val}")
                print("================================================================")
                print("💡 Note on Z-Score: A negative Z-Score indicates the stock is currently")
                print("   statistically undervalued relative to its historical ratio with the benchmark.")
            else:
                print("⚠️ Not enough overlapping historical data points to compute statistics.")

if __name__ == "__main__":
    main()