from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np
from sklearn.metrics import accuracy_score, log_loss

from ai.ensemble import DynamicEnsemble
from ai.models import GradientBoostModel, LSTMProxyModel, RegimeDetectionModel, VolatilityModel


@dataclass
class TrainingResult:
    trained_at: str
    fold_accuracy: float
    fold_logloss: float


class MultiModelTrainer:
    def __init__(self) -> None:
        self.models = [
            GradientBoostModel(),
            LSTMProxyModel(),
            RegimeDetectionModel(),
            VolatilityModel(),
        ]
        self.ensemble = DynamicEnsemble([m.name for m in self.models])

    def walk_forward_train(self, x: np.ndarray, y: np.ndarray, folds: int = 4) -> TrainingResult:
        split_size = len(x) // (folds + 1)
        accs: list[float] = []
        losses: list[float] = []

        for i in range(1, folds + 1):
            train_end = split_size * i
            test_end = split_size * (i + 1)
            x_train, y_train = x[:train_end], y[:train_end]
            x_test, y_test = x[train_end:test_end], y[train_end:test_end]
            if len(x_test) == 0:
                continue

            preds = {}
            for model in self.models:
                model.fit(x_train, y_train)
                preds[model.name] = model.predict_proba(x_test)

            ensemble_pred = self.ensemble.combine(preds)
            self.ensemble.update_weights(y_test, preds)
            accs.append(accuracy_score(y_test, (ensemble_pred > 0.5).astype(int)))
            losses.append(log_loss(y_test, np.vstack([1 - ensemble_pred, ensemble_pred]).T, labels=[0, 1]))

        return TrainingResult(
            trained_at=datetime.utcnow().isoformat(),
            fold_accuracy=float(np.mean(accs) if accs else 0),
            fold_logloss=float(np.mean(losses) if losses else 0),
        )

    def predict_latest_probability(self, x_latest: np.ndarray) -> tuple[float, dict[str, float]]:
        probs = {m.name: m.predict_proba(x_latest)[0] for m in self.models}
        ensemble = sum(self.ensemble.weights[name] * probs[name] for name in probs)
        return float(ensemble), probs
