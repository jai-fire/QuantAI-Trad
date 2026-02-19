from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class PlatformConfig:
    symbol: str = "BTC/USDT:USDT"
    timeframe: str = "5m"
    history_limit: int = 1000
    loop_interval_seconds: int = 15
    paper_trading: bool = True
    enable_training: bool = True
    risk_per_trade: float = 0.01
    max_total_exposure: float = 0.30
    max_daily_loss: float = 0.05
    max_drawdown: float = 0.20
    atr_stop_multiple: float = 1.8
    atr_take_multiple: float = 3.0
    model_retrain_every_n_steps: int = 30
    db_path: Path = Path("database/platform.db")

    def to_dict(self) -> dict:
        values = asdict(self)
        values["db_path"] = str(values["db_path"])
        return values


DEFAULT_CONFIG = PlatformConfig()
