from __future__ import annotations


def fees(notional: float, taker_fee: float = 0.0004) -> float:
    return abs(notional) * taker_fee
