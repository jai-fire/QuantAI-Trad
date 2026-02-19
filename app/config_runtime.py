from database.settings import load_settings

DEFAULTS = {
    "symbol": "BTC/USDT",
    "risk_per_trade": 0.01,
    "loop_interval": 10,
    "paper_trading": True,
    "enable_training": True,
    "starting_balance": 1000
}

CONFIG = DEFAULTS.copy()
CONFIG.update(load_settings())
