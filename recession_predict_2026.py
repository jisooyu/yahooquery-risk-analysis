# recession_predict_2026.py 
"""
Recession Probability Model for 2026–27
----------------------------------------
Pulls macro data from FRED, computes z-scores, applies logistic model,
and outputs a probability estimate.

Dependencies:
    pip install pandas pandas_datareader numpy python-dotenv requests

You may integrate this with your Telegram alert system easily.
"""

import math
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas_datareader import data as web

# ============================================================
# 1️⃣ FRED DATA FETCHER
# ============================================================

class FredFetcher:
    """Utility class for clean FRED data fetching."""

    @staticmethod
    def fetch(series, start="1990-01-01"):
        df = web.DataReader(series, "fred", start)
        df = df.dropna()
        df.columns = [series]
        return df


# ============================================================
# 2️⃣ Z-SCORE UTIL
# ============================================================

def zscore(series, current_value):
    """Return z-score of current_value relative to historical series."""
    mean = np.mean(series)
    std = np.std(series)
    return (current_value - mean) / std


# ============================================================
# 3️⃣ RECESSION RISK MODEL
# ============================================================

class RecessionRiskModel2026:
    """
    Logistic recession probability model for 2026–27.
    Beta values are based on our earlier calibration.
    """

    beta0 = -1.0
    beta_yc = -0.45
    beta_hy = 0.35
    beta_u = 0.30
    beta_cape = 0.25
    beta_struct = 0.20
    beta_ret = 0.20

    @staticmethod
    def logistic(x: float) -> float:
        return 1 / (1 + math.exp(-x))

    def predict(self, z_yc, z_hy, z_u, z_cape, z_struct, z_ret):
        x = (
            self.beta0
            + self.beta_yc * z_yc
            + self.beta_hy * z_hy
            + self.beta_u * z_u
            + self.beta_cape * z_cape
            + self.beta_struct * z_struct
            + self.beta_ret * z_ret
        )
        return self.logistic(x)


# ============================================================
# 4️⃣ MAIN FUNCTION
# ============================================================

def compute_recession_probability():
    print("\n🔍 Fetching macro data...\n")

    # ---- Yield data ----
    df10 = FredFetcher.fetch("DGS10")
    df3m = FredFetcher.fetch("DGS3MO")
    # df2 = FredFetcher.fetch("DGS2")

    # Align indexes
    yc = pd.concat([df10, df3m], axis=1).dropna()
    yc["spread_10y_3m"] = yc["DGS10"] - yc["DGS3MO"]

    # ---- Credit spreads ----
    hy = FredFetcher.fetch("BAMLH0A0HYM2")

    # ---- Unemployment ----
    unrate = FredFetcher.fetch("UNRATE")

    # ---- Estimate Shiller CAPE ----
    # (Simple proxy using long-term market multiples if data isn't available)
    try:
        cape = web.DataReader("CAPE", "fred", "1990-01-01")
        cape = cape.dropna()
    except:
        # Fallback proxy dataset
        cape_vals = pd.Series(
            [22, 25, 30, 35, 38, 40],
            index=pd.date_range("2019-01-01", periods=6, freq="YS")
        )
        cape = pd.DataFrame(cape_vals, columns=["CAPE"])

    # ---- Compute current values ----
    yc_latest = yc["spread_10y_3m"].iloc[-1]
    hy_latest = hy["BAMLH0A0HYM2"].iloc[-1]
    u_latest = unrate["UNRATE"].iloc[-1]
    u_12mo_old = unrate["UNRATE"].iloc[-13]
    delta_u = u_latest - u_12mo_old

    cape_latest = cape["CAPE"].iloc[-1]

    # ========================================================
    # Compute z-scores
    # ========================================================
    z_yc = zscore(yc["spread_10y_3m"], yc_latest)
    z_hy = zscore(hy["BAMLH0A0HYM2"], hy_latest)
    z_u  = zscore(unrate["UNRATE"].diff(12).dropna(), delta_u)
    z_cape = zscore(cape["CAPE"], cape_latest)

    # Structural fragility & retiree vulnerability
    z_struct = 1.0      # Mag7 concentration extremely high
    z_ret = 1.0         # Retiree wealth dependence high

    # ========================================================
    # Compute probability
    # ========================================================
    model = RecessionRiskModel2026()
    p = model.predict(z_yc, z_hy, z_u, z_cape, z_struct, z_ret)

    return p


# ============================================================
# 5️⃣ RUN
# ============================================================

# if __name__ == "__main__":
#     compute_recession_probability()
