# data_fetching.py
import pandas as pd
from yahooquery import Ticker
from pandas_datareader import data as web

# ----------------------------------------------------------
# 1) FRED MACRO SERIES
# ----------------------------------------------------------
FRED_SERIES = {
    "HY_OAS": "BAMLH0A0HYM2",     # ICE BofA High Yield OAS
    "NFCI": "NFCI",               # Chicago Fed Financial Conditions Index
    "TOTALSL": "TOTALSL",         # Consumer Credit
    "DGS2": "DGS2",               # 2Y Treasury yield
    "DGS10": "DGS10",             # 10Y Treasury yield
    "DGS30": "DGS30",             # 30Y Treasury yield
}


def fetch_fred():
    """Fetch FRED macro data with safe fallback."""
    macro = pd.DataFrame()

    for col, fred_code in FRED_SERIES.items():
        try:
            df = web.DataReader(fred_code, "fred")
            df.columns = [col]
            macro = macro.join(df, how="outer")
        except Exception:
            continue

    return macro.ffill()


# ----------------------------------------------------------
# 2) YAHOOQUERY MARKET PRICES
# ----------------------------------------------------------
def fetch_yahoo_prices(ticker_groups):
    tickers = sum(ticker_groups.values(), [])

    tq = Ticker(tickers, asynchronous=True, max_workers=8)
    data = tq.history(period="1y", interval="1d")

    if data is None or data.empty:
        return pd.DataFrame()

    # MultiIndex case: (ticker, date)
    if isinstance(data.index, pd.MultiIndex):

        if "adjclose" in data.columns:
            df = data["adjclose"].unstack(level=0)
        elif "close" in data.columns:
            df = data["close"].unstack(level=0)
        else:
            return pd.DataFrame()

    else:
        if "adjclose" in data.columns:
            df = data[["adjclose"]]
        elif "close" in data.columns:
            df = data[["close"]]
        else:
            return pd.DataFrame()

    df = df.ffill().dropna(how="all")
    df = df[[c for c in df.columns if c in tickers]]
    return df


# ----------------------------------------------------------
# 3) MERGE YAHOO + FRED
# ----------------------------------------------------------
def fetch_data(ticker_groups):
    """
    Unified fetcher:
    - yahooquery market data (ETF, vol, FX)
    - FRED macro data (credit, yields, liquidity)
    """
    yahoo_df = fetch_yahoo_prices(ticker_groups)
    fred_df = fetch_fred()

    if yahoo_df.empty and fred_df.empty:
        return pd.DataFrame()

    # Merge on datetime index
    full = yahoo_df.join(fred_df, how="outer")

    # Forward fill for daily alignment
    return full.ffill()
