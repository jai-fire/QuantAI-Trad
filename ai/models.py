from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression


@dataclass
class ModelOutput:
    name: str
    probs: np.ndarray


class BaseProbModel:
    name = "base"

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        raise NotImplementedError

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class GradientBoostModel(BaseProbModel):
    name = "gradient_boosting"

    def __init__(self) -> None:
        self.model = GradientBoostingClassifier(random_state=42)

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(x, y)

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(x)[:, 1]


class RegimeDetectionModel(BaseProbModel):
    name = "regime_detection"

    def __init__(self) -> None:
        self.model = LogisticRegression(max_iter=400)

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(x, y)

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(x)[:, 1]


class VolatilityModel(BaseProbModel):
    name = "volatility_proxy"

    def __init__(self) -> None:
        self.model = RandomForestClassifier(n_estimators=120, random_state=42)

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(x, y)

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(x)[:, 1]


class LSTMProxyModel(BaseProbModel):
    name = "lstm_proxy"

    def __init__(self) -> None:
        self.model = LogisticRegression(max_iter=500)

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(x, y)

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(x)[:, 1]
