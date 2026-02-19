from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime

import numpy as np

from ai.features import FeatureEngineer
from ai.trainer import MultiModelTrainer
from app.config_runtime import load_runtime_config
from data.collector import CollectorConfig, MarketDataCollector
from database.db import Database
from database.trades import TradeStore
from trading.executor import ExecutionEngine
from trading.metrics import MetricsEngine
from trading.planner import create_trade_plan
from trading.position_manager import Position, PositionManager
from trading.risk import RiskEngine, RiskState

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class TradingPlatform:
    def __init__(self) -> None:
        self.config = load_runtime_config()
        self.db = Database(self.config.db_path)
        self.trade_store = TradeStore(self.db)
        self.collector = MarketDataCollector(
            CollectorConfig(symbol=self.config.symbol, timeframe=self.config.timeframe, limit=self.config.history_limit)
        )
        self.trainer = MultiModelTrainer()
        self.execution = ExecutionEngine(self.config.paper_trading)
        self.positions = PositionManager()
        self.risk = RiskEngine(
            self.config.risk_per_trade,
            self.config.max_total_exposure,
            self.config.max_daily_loss,
            self.config.max_drawdown,
        )
        self.initial_balance = 10_000.0
        self.state = RiskState(balance=self.initial_balance, equity_peak=self.initial_balance)
        self.step_count = 0
        self.last_training = {"accuracy": 0.0, "log_loss": 0.0}

    async def step(self) -> dict:
        market = await self.collector.fetch_ohlcv()
        features = FeatureEngineer.add_all(market)
        x = features[FeatureEngineer.feature_columns()].to_numpy()
        y = features["target"].to_numpy()
        latest = features.iloc[-1]

        if self.config.enable_training and self.step_count % self.config.model_retrain_every_n_steps == 0:
            result = self.trainer.walk_forward_train(x, y)
            self.last_training = {"accuracy": result.fold_accuracy, "log_loss": result.fold_logloss}
            with self.db.cursor() as cur:
                cur.execute(
                    "INSERT INTO model_metrics (created_at, model_name, accuracy, log_loss, brier, metadata) VALUES (?,?,?,?,?,?)",
                    (
                        result.trained_at,
                        "ensemble",
                        result.fold_accuracy,
                        result.fold_logloss,
                        0.0,
                        json.dumps({"weights": self.trainer.ensemble.weights}),
                    ),
                )

        probability, model_probs = self.trainer.predict_latest_probability(x[-1:])
        direction = "LONG" if probability >= 0.5 else "SHORT"
        confidence = abs(probability - 0.5) * 2
        risk_score = float(np.clip(latest["volatility_20"] * 10, 0, 1))

        closed = self.positions.mark_to_market(float(latest["close"]))
        for trade in closed:
            self.state.balance += trade["pnl"]
            self.state.daily_pnl += trade["pnl"]
            self.state.equity_peak = max(self.state.equity_peak, self.state.balance)
            self.trade_store.insert_trade({**trade, "symbol": self.config.symbol, "meta": {"model_probs": model_probs}})

        exposure = sum(p.entry * p.size for p in self.positions.open_positions) / max(self.state.balance, 1)
        allowed, reason = self.risk.approve(self.state, exposure)

        if allowed and confidence > 0.2 and not self.positions.open_positions:
            plan = create_trade_plan(
                float(latest["close"]),
                float(latest["atr"]),
                direction,
                self.state.balance,
                self.config.risk_per_trade,
                self.config.atr_stop_multiple,
                self.config.atr_take_multiple,
            )
            order = {
                "symbol": self.config.symbol,
                "direction": direction,
                **plan,
                "confidence": confidence,
                "risk_score": risk_score,
                "opened_at": datetime.utcnow().isoformat(),
            }
            fill = self.execution.execute(order)
            if fill["status"] in {"FILLED", "SUBMITTED"}:
                self.positions.open(
                    Position(
                        symbol=fill["symbol"],
                        direction=fill["direction"],
                        entry=fill["entry"],
                        stop_loss=fill["stop_loss"],
                        take_profit=fill["take_profit"],
                        size=fill["size"],
                        confidence=fill["confidence"],
                        risk_score=fill["risk_score"],
                        opened_at=fill["opened_at"],
                    )
                )

        metrics = MetricsEngine.compute(self.positions.closed_positions, self.initial_balance, self.state.balance)
        drawdown = max(0.0, (self.state.equity_peak - self.state.balance) / max(self.state.equity_peak, 1e-9))
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO equity_curve (ts, equity, balance, drawdown) VALUES (?,?,?,?)",
                (datetime.utcnow().isoformat(), self.state.balance, self.state.balance, drawdown),
            )

        self.step_count += 1
        snapshot = {
            "symbol": self.config.symbol,
            "price": float(latest["close"]),
            "probability_up": probability,
            "confidence": confidence,
            "risk_gate": reason,
            "open_positions": len(self.positions.open_positions),
            "closed_trades": len(self.positions.closed_positions),
            "balance": self.state.balance,
            "ensemble_weights": self.trainer.ensemble.weights,
            "training": self.last_training,
            "metrics": {
                "total_return": metrics.total_return,
                "win_rate": metrics.win_rate,
                "profit_factor": metrics.profit_factor,
                "sharpe": metrics.sharpe,
                "sortino": metrics.sortino,
                "max_drawdown": metrics.max_drawdown,
            },
        }
        return snapshot

    async def run_forever(self) -> None:
        while True:
            try:
                snapshot = await self.step()
                logging.info("snapshot=%s", json.dumps(snapshot))
            except Exception as exc:
                logging.exception("service_step_failed: %s", exc)
            await asyncio.sleep(self.config.loop_interval_seconds)


def run_service() -> None:
    platform = TradingPlatform()
    asyncio.run(platform.run_forever())
