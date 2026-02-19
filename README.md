# QuantAI-Trad Professional AI Trading Platform

Production-oriented modular trading stack focused on **probabilistic forecasting, adaptive learning, and strict risk controls**.

## Project Structure

- `app/` runtime configuration and orchestration service
- `ai/` feature engineering, model training, ensemble logic
- `data/` market data ingestion (CCXT + synthetic fallback)
- `trading/` signal planning, risk checks, execution, position tracking, performance metrics
- `database/` SQLite schema and repositories
- `dashboard/` PyQt6 multi-tab desktop GUI

## Core Workflow

1. Fetch futures OHLCV data from exchange.
2. Generate technical + regime + volatility features.
3. Walk-forward train multiple probabilistic models.
4. Combine model probabilities using dynamic ensemble weights.
5. Build signal (direction/confidence/risk score).
6. Pass signal through risk gates (drawdown/exposure/daily loss).
7. Create trade plan (entry/SL/TP/size/RR).
8. Execute in paper/live mode and manage lifecycle.
9. Persist trades, model-metrics, and equity snapshots for monitoring and analysis.

## Database Schema

`database/db.py` initializes:
- `market_data`
- `feature_data`
- `trades`
- `model_metrics`
- `equity_curve`
- `settings`
- `logs`

## Quick Download Bundle

To generate a distributable ZIP of the full program:

```bash
bash scripts/create_download_bundle.sh
```

Output: `dist/QuantAI-Trad-full-program.zip`

## Run Instructions

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m dashboard.app   # GUI
# or
python -m app.main        # headless async service
```

## Retraining

Retraining happens automatically every `model_retrain_every_n_steps` service ticks.
You can tune:
- `enable_training`
- `model_retrain_every_n_steps`
- `history_limit`

in `app/config.py` or via persisted settings.

## Performance Improvement Guidance

- Add exchange-specific futures metadata (funding, open interest, basis).
- Add order-book imbalance and trade-flow features.
- Replace LSTM proxy with true PyTorch sequence model + checkpointing.
- Use PostgreSQL + message queue for horizontal scaling.
- Add Bayesian/online weight updates for ensemble.
- Add realistic transaction cost and slippage models.

## Limitations

- No guarantee of profits; outputs are probabilistic.
- Synthetic fallback data is used when exchange requests fail.
- Current live mode is connectivity-ready but intentionally conservative.
- GUI is desktop-only; not web-distributed.

## Security

- Keep exchange keys outside source code (OS keychain or secrets manager).
- Require explicit operator confirmation before any live deployment.
- Audit logs and role-based access should be added for team environments.
