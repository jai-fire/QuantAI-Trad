def create_trade(price, atr, direction, balance, risk):

    risk_amt = balance * risk

    if direction == "BUY":
        sl = price - atr*1.5
        tp = price + atr*3
    else:
        sl = price + atr*1.5
        tp = price - atr*3

    size = risk_amt / abs(price-sl)

    return {"entry": price, "sl": sl, "tp": tp, "size": size}
