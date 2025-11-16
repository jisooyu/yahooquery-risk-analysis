# data_fetching.py
from yahooquery import Ticker
import pandas as pd

def fetch_data(ticker_groups):
    """
    Fetch multi-ticker daily close prices using yahooquery.
    This avoids the heavy rate limits of yfinance and is Render-friendly.
    """

    # Flatten ticker list
    tickers = sum(ticker_groups.values(), [])

    # Use yahooquery - much more reliable and no rate limits
    tq = Ticker(tickers, asynchronous=True, max_workers=8)

    # Fetch 1-year daily historical data
    data = tq.history(period="1y", interval="1d")

    # If yahooquery fails completely
    if data is None or data.empty:
        return pd.DataFrame()

    # ----------------------------------------------------------
    # yahooquery returns a MultiIndex: (ticker, date)
    # or a DataFrame with MultiIndex columns
    # ----------------------------------------------------------

    # If history returned series for multiple tickers:
    # Format:
    #   close  open ...
    # ticker  date
    if isinstance(data.index, pd.MultiIndex):

        # pivot close prices into columns
        if "close" in data.columns:
            df = data["close"].unstack(level=0)
        else:
            # some ETFs may use 'adjclose'
            df = data["adjclose"].unstack(level=0)

    else:
        # Single ticker edge case
        if "close" in data.columns:
            df = data[["close"]]
        else:
            df = data[["adjclose"]]

    # Cleanup: forward-fill + drop full-empty columns
    df = df.ffill().dropna(how="all")

    # Keep only tickers Yahoo actually returned
    df = df[[c for c in df.columns if c in tickers]]

    return df
