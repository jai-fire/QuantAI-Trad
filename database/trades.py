import sqlite3

conn = sqlite3.connect("database/trades.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY,
    time TEXT,
    direction TEXT,
    entry REAL,
    exit REAL,
    pnl REAL,
    size REAL,
    status TEXT
)
""")

def log_trade(trade):
    cursor.execute(
        "INSERT INTO trades (time,direction,entry,exit,pnl,size,status) VALUES (?,?,?,?,?,?,?)",
        (trade["time"], trade["direction"], trade["entry"], trade["exit"], trade["pnl"], trade["size"], trade["status"])
    )
    conn.commit()
