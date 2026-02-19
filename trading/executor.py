from __future__ import annotations


class ExecutionEngine:
    def __init__(self, paper_mode: bool = True) -> None:
        self.paper_mode = paper_mode

    def execute(self, order: dict) -> dict:
        if self.paper_mode:
            return {**order, "execution_mode": "paper", "status": "FILLED"}
        return {**order, "execution_mode": "live", "status": "SUBMITTED"}
