from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass

import numpy as np
import pandas as pd

try:
    import ccxt.async_support as ccxt
except Exception:  # pragma: no cover
    ccxt = None


@dataclass
class CollectorConfig:
    symbol: str
    timeframe: str
    limit: int = 1000


class MarketDataCollector:
    def __init__(self, config: CollectorConfig) -> None:
        self.config = config
        self.exchange = ccxt.binanceusdm() if ccxt else None

    async def fetch_ohlcv(self) -> pd.DataFrame:
        if self.exchange is None:
            return self._synthetic_data()
        try:
            data = await self.exchange.fetch_ohlcv(
                self.config.symbol,
                timeframe=self.config.timeframe,
                limit=self.config.limit,
            )
            df = pd.DataFrame(data, columns=["ts", "open", "high", "low", "close", "volume"])
            return df
        except Exception:
            return self._synthetic_data()

    async def close(self) -> None:
        if self.exchange is not None:
            await self.exchange.close()

    def _synthetic_data(self) -> pd.DataFrame:
        n = self.config.limit
        base = 100 + np.cumsum(np.random.normal(0, 0.5, size=n))
        high = base + np.abs(np.random.normal(0, 0.7, size=n))
        low = base - np.abs(np.random.normal(0, 0.7, size=n))
        ts = np.arange(n) * 60_000 + int(time.time() * 1000) - n * 60_000
        return pd.DataFrame(
            {
                "ts": ts,
                "open": base,
                "high": high,
                "low": low,
                "close": base + np.random.normal(0, 0.3, size=n),
                "volume": np.abs(np.random.normal(100, 20, size=n)),
            }
        )
