from __future__ import annotations

import numpy as np
import pandas as pd


class FeatureEngineer:
    @staticmethod
    def add_all(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        c = out["close"]
        h = out["high"]
        l = out["low"]

        out["sma_10"] = c.rolling(10).mean()
        out["sma_30"] = c.rolling(30).mean()
        out["ema_12"] = c.ewm(span=12, adjust=False).mean()
        out["ema_26"] = c.ewm(span=26, adjust=False).mean()

        delta = c.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = -delta.clip(upper=0).rolling(14).mean()
        rs = gain / (loss.replace(0, np.nan))
        out["rsi"] = 100 - (100 / (1 + rs))

        out["macd"] = out["ema_12"] - out["ema_26"]
        out["macd_signal"] = out["macd"].ewm(span=9, adjust=False).mean()

        tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
        out["atr"] = tr.rolling(14).mean()

        mavg = c.rolling(20).mean()
        mstd = c.rolling(20).std()
        out["bb_upper"] = mavg + 2 * mstd
        out["bb_lower"] = mavg - 2 * mstd
        out["bb_width"] = (out["bb_upper"] - out["bb_lower"]) / mavg

        out["momentum_5"] = c.pct_change(5)
        out["momentum_10"] = c.pct_change(10)
        out["volatility_20"] = c.pct_change().rolling(20).std()

        trend_raw = (out["sma_10"] - out["sma_30"]) / out["sma_30"]
        out["trend_strength"] = trend_raw.abs()
        out["regime_feature"] = np.where(trend_raw > 0.001, 1, np.where(trend_raw < -0.001, -1, 0))

        out["target"] = (out["close"].shift(-1) > out["close"]).astype(int)
        return out.dropna().reset_index(drop=True)

    @staticmethod
    def feature_columns() -> list[str]:
        return [
            "open", "high", "low", "close", "volume", "sma_10", "sma_30", "ema_12", "ema_26",
            "rsi", "macd", "macd_signal", "atr", "bb_upper", "bb_lower", "bb_width",
            "momentum_5", "momentum_10", "volatility_20", "trend_strength", "regime_feature",
        ]
