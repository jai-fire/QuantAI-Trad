from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskState:
    balance: float
    equity_peak: float
    daily_pnl: float = 0.0


class RiskEngine:
    def __init__(self, risk_per_trade: float, max_exposure: float, max_daily_loss: float, max_drawdown: float) -> None:
        self.risk_per_trade = risk_per_trade
        self.max_exposure = max_exposure
        self.max_daily_loss = max_daily_loss
        self.max_drawdown = max_drawdown

    def approve(self, state: RiskState, current_exposure: float) -> tuple[bool, str]:
        dd = max(0.0, (state.equity_peak - state.balance) / max(state.equity_peak, 1e-9))
        if dd >= self.max_drawdown:
            return False, "max_drawdown"
        if abs(state.daily_pnl) >= state.balance * self.max_daily_loss:
            return False, "daily_loss_limit"
        if current_exposure >= self.max_exposure:
            return False, "max_exposure"
        return True, "ok"
