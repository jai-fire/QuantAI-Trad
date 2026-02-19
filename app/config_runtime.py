from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from app.config import DEFAULT_CONFIG, PlatformConfig
from database.settings import load_settings


def load_runtime_config() -> PlatformConfig:
    cfg = replace(DEFAULT_CONFIG)
    settings = load_settings()
    for key, raw in settings.items():
        if not hasattr(cfg, key):
            continue
        current = getattr(cfg, key)
        if isinstance(current, bool):
            value = str(raw).lower() in {"1", "true", "yes", "on"}
        elif isinstance(current, int):
            value = int(raw)
        elif isinstance(current, float):
            value = float(raw)
        elif isinstance(current, Path):
            value = Path(raw)
        else:
            value = raw
        setattr(cfg, key, value)
    return cfg
