from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path


class Database:
    def __init__(self, path: str | Path = "database/platform.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY,
                ts INTEGER,
                symbol TEXT,
                timeframe TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL
            );
            CREATE TABLE IF NOT EXISTS feature_data (
                id INTEGER PRIMARY KEY,
                ts INTEGER,
                symbol TEXT,
                payload TEXT
            );
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY,
                opened_at TEXT,
                closed_at TEXT,
                symbol TEXT,
                direction TEXT,
                entry REAL,
                exit REAL,
                stop_loss REAL,
                take_profit REAL,
                size REAL,
                fees REAL,
                pnl REAL,
                confidence REAL,
                risk_score REAL,
                status TEXT,
                meta TEXT
            );
            CREATE TABLE IF NOT EXISTS model_metrics (
                id INTEGER PRIMARY KEY,
                created_at TEXT,
                model_name TEXT,
                accuracy REAL,
                log_loss REAL,
                brier REAL,
                metadata TEXT
            );
            CREATE TABLE IF NOT EXISTS equity_curve (
                id INTEGER PRIMARY KEY,
                ts TEXT,
                equity REAL,
                balance REAL,
                drawdown REAL
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                ts TEXT,
                level TEXT,
                component TEXT,
                message TEXT
            );
            """
        )
        self.conn.commit()

    @contextmanager
    def cursor(self):
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        finally:
            cur.close()
