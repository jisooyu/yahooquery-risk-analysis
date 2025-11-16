# app.py
from dash import Dash
from layout import build_layout
from callbacks import register_callbacks

# Working tickers only
RISK_TICKERS = {
    "Signal Guide": [],
    "Volatility": ["^VIX", "^VIX3M", "^VIX6M", "^VXN", "^SKEW"],
    "Credit Risk": ["HYG", "JNK", "LQD"],
    "Treasury Yields": ["^FVX", "^TNX", "^TYX"],
    "Liquidity": ["UUP", "SHY", "IEI"],
    "Global Risk": ["EEM"],
    "Stress Score": [],
}

app = Dash(__name__)
app.layout = build_layout(RISK_TICKERS)

register_callbacks(app, RISK_TICKERS)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8050, debug=True)
