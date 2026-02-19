open_position = None

def open_trade(trade):
    global open_position
    open_position = trade
    return open_position

def update_position(price):

    global open_position

    if not open_position:
        return None

    if open_position["direction"] == "BUY":
        if price <= open_position["sl"] or price >= open_position["tp"]:
            return close_trade(price)

    else:
        if price >= open_position["sl"] or price <= open_position["tp"]:
            return close_trade(price)

    return None

def close_trade(price):

    global open_position

    open_position["exit"] = price
    open_position["pnl"] = (price - open_position["entry"]) * open_position["size"]
    open_position["status"] = "CLOSED"

    closed = open_position
    open_position = None
    return closed
