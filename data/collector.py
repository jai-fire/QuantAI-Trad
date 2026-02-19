import ccxt
import pandas as pd
from app.config import CONFIG

exchange = ccxt.coinex()

def fetch_data(limit=300):
    data = exchange.fetch_ohlcv(CONFIG["symbol"], CONFIG["timeframe"], limit=limit)
    df = pd.DataFrame(data, columns=["time","open","high","low","close","volume"])
    return df
