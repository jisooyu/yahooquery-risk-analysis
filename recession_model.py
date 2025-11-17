# recession_model.py
import math
import pandas as pd
import numpy as np
from pandas_datareader import data as web

# -----------------------------------------------------------
# FRED fetch util
# -----------------------------------------------------------

def fred(series, start="1990-01-01"):
    df = web.DataReader(series, "fred", start)
    df.columns = [series]
    return df.dropna()


# -----------------------------------------------------------
# Z-score
# -----------------------------------------------------------

def zscore(series, current):
    return (current - series.mean()) / series.std()


# -----------------------------------------------------------
# Recession Model class
# -----------------------------------------------------------

class RecessionRiskModel2026:
    beta0 = -1.0
    beta_yc = -0.45
    beta_hy = 0.35
    beta_u = 0.30
    beta_cape = 0.25
    beta_struct = 0.20
    beta_ret = 0.20

    @staticmethod
    def logistic(x):
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


# -----------------------------------------------------------
# Compute full recession probability
# -----------------------------------------------------------

def compute_recession_probability():
    # Yield curve (10Y - 3M)
    df10 = fred("DGS10")
    df3m = fred("DGS3MO")

    yc = pd.concat([df10, df3m], axis=1).dropna()
    yc["spread"] = yc["DGS10"] - yc["DGS3MO"]

    # HY Spread
    hy = fred("BAMLH0A0HYM2")

    # Unemployment
    un = fred("UNRATE")
    delta_u = un["UNRATE"].iloc[-1] - un["UNRATE"].iloc[-13]

    # CAPE (fallback)
    try:
        cape = fred("CAPE")
    except:
        cape_vals = pd.Series([22, 25, 30, 35, 38, 40],
                              index=pd.date_range("2019-01-01", periods=6, freq="YS"))
        cape = pd.DataFrame(cape_vals, columns=["CAPE"])

    # Z-scores
    z_yc = zscore(yc["spread"], yc["spread"].iloc[-1])
    z_hy = zscore(hy["BAMLH0A0HYM2"], hy["BAMLH0A0HYM2"].iloc[-1])
    z_u = zscore(un["UNRATE"].diff(12).dropna(), delta_u)
    z_cape = zscore(cape["CAPE"], cape["CAPE"].iloc[-1])

    z_struct = 1.0
    z_ret = 1.0

    model = RecessionRiskModel2026()
    p = model.predict(z_yc, z_hy, z_u, z_cape, z_struct, z_ret)

    return {
        "probability": p,
        "z": {
            "Yield Curve": z_yc,
            "HY Spread": z_hy,
            "Unemployment Δ12M": z_u,
            "CAPE": z_cape,
            "Structural": z_struct,
            "Retiree Wealth": z_ret,
        },
        "raw": {
            "spread": yc["spread"],
            "hy": hy["BAMLH0A0HYM2"],
            "unrate": un["UNRATE"],
            "cape": cape["CAPE"]
        }
    }
