import sqlite3

conn = sqlite3.connect("database/settings.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")

def save_setting(key, value):
    cursor.execute("REPLACE INTO settings VALUES (?,?)",(key,str(value)))
    conn.commit()

def load_settings():
    cursor.execute("SELECT key,value FROM settings")
    return dict(cursor.fetchall())
