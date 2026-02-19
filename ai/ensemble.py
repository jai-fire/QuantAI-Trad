from __future__ import annotations

import numpy as np


class DynamicEnsemble:
    def __init__(self, model_names: list[str]) -> None:
        self.weights = {name: 1 / len(model_names) for name in model_names}
        self.scores = {name: [] for name in model_names}

    def combine(self, probs: dict[str, np.ndarray]) -> np.ndarray:
        total = np.zeros_like(next(iter(probs.values())))
        for name, pred in probs.items():
            total += self.weights.get(name, 0) * pred
        return np.clip(total, 0, 1)

    def update_weights(self, y_true: np.ndarray, probs: dict[str, np.ndarray]) -> None:
        losses = {}
        for name, pred in probs.items():
            brier = float(np.mean((pred - y_true) ** 2))
            self.scores[name].append(brier)
            losses[name] = max(brier, 1e-6)
        inv = {k: 1 / v for k, v in losses.items()}
        norm = sum(inv.values())
        self.weights = {k: v / norm for k, v in inv.items()}
