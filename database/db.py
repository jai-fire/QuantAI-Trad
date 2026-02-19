import sqlite3

conn = sqlite3.connect("database/trades.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY,
    time TEXT,
    direction TEXT,
    entry REAL,
    sl REAL,
    tp REAL,
    size REAL
)
""")

def log_trade(trade):
    cursor.execute(
        "INSERT INTO trades (time, direction, entry, sl, tp, size) VALUES (?, ?, ?, ?, ?, ?)",
        (trade["time"], trade["direction"], trade["entry"], trade["sl"], trade["tp"], trade["size"])
    )
    conn.commit()
