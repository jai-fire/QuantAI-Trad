from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Position:
    symbol: str
    direction: str
    entry: float
    stop_loss: float
    take_profit: float
    size: float
    confidence: float
    risk_score: float
    opened_at: str


class PositionManager:
    def __init__(self) -> None:
        self.open_positions: list[Position] = []
        self.closed_positions: list[dict] = []

    def open(self, position: Position) -> None:
        self.open_positions.append(position)

    def mark_to_market(self, price: float) -> list[dict]:
        closed: list[dict] = []
        survivors: list[Position] = []
        for p in self.open_positions:
            hit = (p.direction == "LONG" and (price <= p.stop_loss or price >= p.take_profit)) or (
                p.direction == "SHORT" and (price >= p.stop_loss or price <= p.take_profit)
            )
            if not hit:
                survivors.append(p)
                continue
            pnl = (price - p.entry) * p.size if p.direction == "LONG" else (p.entry - price) * p.size
            record = {
                **asdict(p),
                "exit": price,
                "closed_at": datetime.utcnow().isoformat(),
                "pnl": pnl,
                "status": "CLOSED",
            }
            closed.append(record)
            self.closed_positions.append(record)
        self.open_positions = survivors
        return closed
