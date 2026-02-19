import time
from data.collector import fetch_data
from ai.features import add_features
from ai.trainer import train_model
from ai.predictor import load_model
from trading.planner import create_trade
from trading.position_manager import open_trade, update_position
from database.trades import log_trade
from app.config_runtime import CONFIG

model = None

def run_service():

    global model

    while True:

        df = fetch_data()
        df = add_features(df)

        df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)
        df.dropna(inplace=True)

        X = df[["open","high","low","close","volume","rsi","atr"]]
        y = df["target"]

        if CONFIG["enable_training"]:
            train_model(X, y)

        model = load_model()

        pred = model.predict(X.tail(1))[0]
        direction = "BUY" if pred == 1 else "SELL"

        price = df.iloc[-1]["close"]
        atr = df.iloc[-1]["atr"]

        closed = update_position(price)

        if closed:
            log_trade(closed)

        else:
            trade = create_trade(price, atr, direction, CONFIG["starting_balance"], CONFIG["risk_per_trade"])
            trade["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            trade["direction"] = direction
            trade["status"] = "OPEN"
            open_trade(trade)

        time.sleep(CONFIG["loop_interval"])
