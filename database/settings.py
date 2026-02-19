from __future__ import annotations

from database.db import Database

_db = Database()


def save_setting(key: str, value: str) -> None:
    with _db.cursor() as cur:
        cur.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))


def load_settings() -> dict[str, str]:
    with _db.cursor() as cur:
        rows = cur.execute("SELECT key, value FROM settings").fetchall()
    return {r["key"]: r["value"] for r in rows}
