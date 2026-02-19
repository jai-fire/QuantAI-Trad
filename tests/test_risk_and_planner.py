import unittest

from trading.planner import create_trade_plan
from trading.risk import RiskEngine, RiskState


class RiskPlannerTests(unittest.TestCase):
    def test_trade_plan_rr_positive(self):
        plan = create_trade_plan(100.0, 2.0, "LONG", 10_000.0, 0.01, 1.5, 3.0)
        self.assertGreater(plan["size"], 0)
        self.assertGreater(plan["risk_reward"], 1)
        self.assertLess(plan["stop_loss"], plan["entry"])
        self.assertGreater(plan["take_profit"], plan["entry"])

    def test_risk_gate_drawdown(self):
        engine = RiskEngine(0.01, 0.3, 0.05, 0.2)
        state = RiskState(balance=70, equity_peak=100, daily_pnl=0)
        allowed, reason = engine.approve(state, 0.1)
        self.assertFalse(allowed)
        self.assertEqual(reason, "max_drawdown")


if __name__ == "__main__":
    unittest.main()
