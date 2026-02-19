from __future__ import annotations

import asyncio
import json
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.service import TradingPlatform


class TradingDashboard(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QuantAI Trad Platform")
        self.resize(1200, 760)
        self.platform = TradingPlatform()
        self.snapshot = {}

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.overview = self._build_overview_tab()
        self.market = self._build_market_tab()
        self.trading = self._build_trading_tab()
        self.models = self._build_model_tab()
        self.risk = self._build_risk_tab()
        self.settings = self._build_settings_tab()
        self.logs = self._build_logs_tab()

        self.tabs.addTab(self.overview, "Overview")
        self.tabs.addTab(self.market, "Market")
        self.tabs.addTab(self.trading, "Trading")
        self.tabs.addTab(self.models, "AI Models")
        self.tabs.addTab(self.risk, "Risk")
        self.tabs.addTab(self.settings, "Settings")
        self.tabs.addTab(self.logs, "Logs")

        self.timer = QTimer(self)
        self.timer.setInterval(self.platform.config.loop_interval_seconds * 1000)
        self.timer.timeout.connect(self.refresh)
        self.timer.start()
        self.refresh()

    def _build_overview_tab(self) -> QWidget:
        w = QWidget()
        self.balance_label = QLabel("Balance: --")
        self.confidence_label = QLabel("Confidence: --")
        self.return_label = QLabel("Total Return: --")
        self.status_label = QLabel("System Status: Running")
        layout = QVBoxLayout()
        layout.addWidget(self.balance_label)
        layout.addWidget(self.confidence_label)
        layout.addWidget(self.return_label)
        layout.addWidget(self.status_label)
        w.setLayout(layout)
        return w

    def _build_market_tab(self) -> QWidget:
        w = QWidget()
        self.price_label = QLabel("Price: --")
        self.prob_label = QLabel("P(up): --")
        layout = QVBoxLayout()
        layout.addWidget(self.price_label)
        layout.addWidget(self.prob_label)
        w.setLayout(layout)
        return w

    def _build_trading_tab(self) -> QWidget:
        w = QWidget()
        self.trade_table = QTableWidget(0, 6)
        self.trade_table.setHorizontalHeaderLabels(["Open Time", "Dir", "Entry", "SL", "TP", "Size"])
        layout = QVBoxLayout()
        layout.addWidget(self.trade_table)
        w.setLayout(layout)
        return w

    def _build_model_tab(self) -> QWidget:
        w = QWidget()
        self.weights_text = QTextEdit()
        self.weights_text.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ensemble Weights / Training Metrics"))
        layout.addWidget(self.weights_text)
        w.setLayout(layout)
        return w

    def _build_risk_tab(self) -> QWidget:
        w = QWidget()
        self.risk_label = QLabel("Risk Gate: --")
        layout = QVBoxLayout()
        layout.addWidget(self.risk_label)
        w.setLayout(layout)
        return w

    def _build_settings_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout()
        form.addRow("Symbol", QLabel(self.platform.config.symbol))
        form.addRow("Timeframe", QLabel(self.platform.config.timeframe))
        form.addRow("Mode", QLabel("Paper" if self.platform.config.paper_trading else "Live"))
        w.setLayout(form)
        return w

    def _build_logs_tab(self) -> QWidget:
        w = QWidget()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.log_text.clear)
        layout = QVBoxLayout()
        layout.addWidget(self.log_text)
        layout.addWidget(clear_btn)
        w.setLayout(layout)
        return w

    def refresh(self) -> None:
        try:
            self.snapshot = asyncio.run(self.platform.step())
            self._render_snapshot()
        except Exception as exc:
            self.log_text.append(f"error: {exc}")

    def _render_snapshot(self) -> None:
        s = self.snapshot
        self.balance_label.setText(f"Balance: {s['balance']:.2f}")
        self.confidence_label.setText(f"Confidence: {s['confidence']:.2f}")
        self.return_label.setText(f"Total Return: {s['metrics']['total_return']:.2%}")
        self.price_label.setText(f"Price: {s['price']:.2f}")
        self.prob_label.setText(f"P(up): {s['probability_up']:.2%}")
        self.risk_label.setText(f"Risk Gate: {s['risk_gate']}")
        self.weights_text.setText(json.dumps({"weights": s["ensemble_weights"], "training": s["training"]}, indent=2))
        self.log_text.append(json.dumps(s))

        positions = self.platform.positions.open_positions
        self.trade_table.setRowCount(len(positions))
        for i, p in enumerate(positions):
            self.trade_table.setItem(i, 0, QTableWidgetItem(p.opened_at))
            self.trade_table.setItem(i, 1, QTableWidgetItem(p.direction))
            self.trade_table.setItem(i, 2, QTableWidgetItem(f"{p.entry:.2f}"))
            self.trade_table.setItem(i, 3, QTableWidgetItem(f"{p.stop_loss:.2f}"))
            self.trade_table.setItem(i, 4, QTableWidgetItem(f"{p.take_profit:.2f}"))
            self.trade_table.setItem(i, 5, QTableWidgetItem(f"{p.size:.4f}"))


def main() -> None:
    app = QApplication(sys.argv)
    win = TradingDashboard()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
