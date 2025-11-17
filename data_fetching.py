# data_fetching.py
from yahooquery import Ticker
import pandas as pd

def fetch_data(ticker_groups):
    """
    Fetch multi-ticker daily prices using yahooquery.
    Always prefer adjclose to match yfinance.
    """

    tickers = sum(ticker_groups.values(), [])

    tq = Ticker(tickers, asynchronous=True, max_workers=8)

    # Fetch historical OHLCV
    data = tq.history(period="1y", interval="1d")

    if data is None or data.empty:
        return pd.DataFrame()

    # ----------------------------------------------------------
    # yahooquery usually returns MultiIndex (ticker, date)
    # ----------------------------------------------------------
    if isinstance(data.index, pd.MultiIndex):

        # Prefer adjclose if present
        if "adjclose" in data.columns:
            df = data["adjclose"].unstack(level=0)

        # Fall back to close only when required
        elif "close" in data.columns:
            df = data["close"].unstack(level=0)

        else:
            return pd.DataFrame()

    else:
        # Single ticker case
        if "adjclose" in data.columns:
            df = data[["adjclose"]]
        elif "close" in data.columns:
            df = data[["close"]]
        else:
            return pd.DataFrame()

    df = df.ffill().dropna(how="all")

    # Keep only requested tickers
    df = df[[col for col in df.columns if col in tickers]]

    return df
