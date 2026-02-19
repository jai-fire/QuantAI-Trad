import sys, os
import streamlit as st
import pandas as pd
import sqlite3

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from app.config_runtime import CONFIG
from database.settings import save_setting

st.set_page_config(layout="wide")
st.title("🚀 Pro Trading Platform")

conn = sqlite3.connect("database/trades.db")
df = pd.read_sql("SELECT * FROM trades", conn)

tabs = st.tabs(["Overview","Positions","Performance","Settings","AI Status"])

# ======================
with tabs[0]:
    st.header("Overview")
    st.metric("Balance", CONFIG["starting_balance"])
    st.metric("Trades", len(df))

# ======================
with tabs[1]:
    st.header("Trades")
    st.dataframe(df)

# ======================
with tabs[2]:
    st.header("Performance")
    if not df.empty:
        st.metric("Total PnL", df["pnl"].sum())

# ======================
with tabs[3]:
    st.header("Settings")

    risk = st.slider("Risk per trade", 0.001,0.05,CONFIG["risk_per_trade"])
    loop = st.slider("Loop interval",5,60,CONFIG["loop_interval"])

    if st.button("Save Settings"):
        save_setting("risk_per_trade", risk)
        save_setting("loop_interval", loop)
        st.success("Saved")

# ======================
with tabs[4]:
    st.header("AI Model")
    if os.path.exists("models/model.pkl"):
        st.success("Model loaded")
    else:
        st.warning("Model missing")
