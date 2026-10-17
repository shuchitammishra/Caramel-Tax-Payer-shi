import io
import time
import requests
import pandas as pd
import yfinance as yf

def fetch_nse_tickers():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            return [str(sym).strip() + ".NS" for sym in df['SYMBOL'].dropna().tolist()]
    except Exception as e:
        print(f"⚠️ Error downloading NSE registry: {e}")
    return ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "SBIN.NS"]

def scan_undervalued_stocks(tickers, criteria, limit=100):
    undervalued_stocks = []
    if limit:
        tickers = tickers[:limit]
        
    print(f"🔍 Screening first {len(tickers)} stocks for value metrics...")
    for i, ticker in enumerate(tickers, 1):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            pe = info.get('trailingPE')
            pb = info.get('priceToBook')
            de = info.get('debtToEquity')
            roe = info.get('returnOnEquity')

            de_ratio = (de / 100.0) if de is not None else None
            roe_pct = (roe * 100.0) if roe is not None else None

            if pe is None or pb is None or pe <= 0 or pb <= 0:
                continue

            if pe <= criteria['max_pe'] and pb <= criteria['max_pb'] and \
               (de_ratio is None or de_ratio <= criteria['max_debt_to_equity']) and \
               (roe_pct is None or roe_pct >= criteria['min_roeg']):
                
                undervalued_stocks.append({
                    'Ticker': ticker,
                    'Name': info.get('shortName', ticker),
                    'P/E': round(pe, 2),
                    'P/B': round(pb, 2),
                    'ROE (%)': round(roe_pct, 2) if roe_pct else 'N/A'
                })
        except Exception:
            pass
        time.sleep(0.02)
        
    return pd.DataFrame(undervalued_stocks)