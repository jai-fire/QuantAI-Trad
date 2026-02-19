import ta

def add_features(df):
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    df["atr"] = ta.volatility.AverageTrueRange(df["high"], df["low"], df["close"]).average_true_range()
    df.dropna(inplace=True)
    return df
