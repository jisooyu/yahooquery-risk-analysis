# cache.py
import pandas as pd
import time
from pathlib import Path

CACHE_FILE = Path("cached_data.parquet")
CACHE_TTL = 3600  # 1 hour

def load_cache():
    if CACHE_FILE.exists():
        age = time.time() - CACHE_FILE.stat().st_mtime
        if age < CACHE_TTL:
            return pd.read_parquet(CACHE_FILE)
    return None

def save_cache(df):
    df.to_parquet(CACHE_FILE)
