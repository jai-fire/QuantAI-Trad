from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass
class PerformanceMetrics:
    total_return: float
    win_rate: float
    profit_factor: float
    sharpe: float
    sortino: float
    max_drawdown: float
    trades: int


class MetricsEngine:
    @staticmethod
    def compute(closed_trades: list[dict], initial_balance: float, current_balance: float) -> PerformanceMetrics:
        pnls = [float(t.get("pnl", 0.0)) for t in closed_trades]
        trades = len(pnls)
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]
        total_return = (current_balance - initial_balance) / max(initial_balance, 1e-9)
        win_rate = len(wins) / trades if trades else 0.0
        profit_factor = (sum(wins) / abs(sum(losses))) if losses else (float("inf") if wins else 0.0)

        if trades > 1:
            mean = sum(pnls) / trades
            var = sum((p - mean) ** 2 for p in pnls) / (trades - 1)
            std = var ** 0.5
            neg = [p for p in pnls if p < 0]
            neg_std = (sum((p - 0.0) ** 2 for p in neg) / len(neg)) ** 0.5 if neg else 0.0
            sharpe = (mean / std) * sqrt(trades) if std > 0 else 0.0
            sortino = (mean / neg_std) * sqrt(trades) if neg_std > 0 else 0.0
        else:
            sharpe = 0.0
            sortino = 0.0

        equity = initial_balance
        peak = initial_balance
        max_dd = 0.0
        for p in pnls:
            equity += p
            peak = max(peak, equity)
            dd = (peak - equity) / max(peak, 1e-9)
            max_dd = max(max_dd, dd)

        return PerformanceMetrics(total_return, win_rate, profit_factor, sharpe, sortino, max_dd, trades)
