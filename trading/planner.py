from __future__ import annotations


def create_trade_plan(price: float, atr: float, direction: str, balance: float, risk_per_trade: float, atr_stop_multiple: float, atr_take_multiple: float) -> dict:
    risk_amount = balance * risk_per_trade
    stop_distance = max(atr * atr_stop_multiple, price * 0.002)
    tp_distance = max(atr * atr_take_multiple, price * 0.003)

    if direction == "LONG":
        stop_loss = price - stop_distance
        take_profit = price + tp_distance
    else:
        stop_loss = price + stop_distance
        take_profit = price - tp_distance

    position_size = risk_amount / max(abs(price - stop_loss), 1e-9)
    rr = abs(take_profit - price) / max(abs(price - stop_loss), 1e-9)
    return {
        "entry": price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "size": position_size,
        "risk_reward": rr,
    }
