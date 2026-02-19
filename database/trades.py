from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from database.db import Database


class TradeStore:
    def __init__(self, db: Database) -> None:
        self.db = db

    def insert_trade(self, trade: dict[str, Any]) -> None:
        with self.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO trades (
                    opened_at, closed_at, symbol, direction, entry, exit,
                    stop_loss, take_profit, size, fees, pnl, confidence,
                    risk_score, status, meta
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trade.get("opened_at"),
                    trade.get("closed_at"),
                    trade.get("symbol"),
                    trade.get("direction"),
                    trade.get("entry"),
                    trade.get("exit"),
                    trade.get("stop_loss"),
                    trade.get("take_profit"),
                    trade.get("size"),
                    trade.get("fees", 0.0),
                    trade.get("pnl", 0.0),
                    trade.get("confidence", 0.0),
                    trade.get("risk_score", 0.0),
                    trade.get("status"),
                    json.dumps(trade.get("meta", {})),
                ),
            )

    def list_recent(self, limit: int = 200) -> list[dict[str, Any]]:
        with self.db.cursor() as cur:
            rows = cur.execute("SELECT * FROM trades ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]
