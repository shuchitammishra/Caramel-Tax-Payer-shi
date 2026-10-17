# Popular Benchmark Indices / ETFs on Yahoo Finance
POPULAR_BENCHMARKS = {
    "1": {"name": "NIFTY 50 Index (^NSEI)", "symbol": "^NSEI"},
    "2": {"name": "NIFTY 500 Index (^CRSLDX)", "symbol": "^CRSLDX"},
    "3": {"name": "NIFTY Bank Index (^NSEBANK)", "symbol": "^NSEBANK"},
    "4": {"name": "NIFTY IT Index (^CNXIT)", "symbol": "^CNXIT"},
    "5": {"name": "NIFTY BEES ETF (NIFTYBEES.NS)", "symbol": "NIFTYBEES.NS"},
    "6": {"name": "BANK BEES ETF (BANKBEES.NS)", "symbol": "BANKBEES.NS"}
}

# Screening criteria for undervalued stocks
SCREENING_CRITERIA = {
    "max_pe": 20.0,
    "max_pb": 2.5,
    "max_debt_to_equity": 0.5,
    "min_roeg": 10.0
}

# Default historical period for backtesting
DEFAULT_PERIOD = "1y" # Options: '6m', '1y', '2y', '5y'