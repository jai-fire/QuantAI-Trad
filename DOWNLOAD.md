# Download the Full Program

This repository includes a complete source bundle script.

## Option 1: Create ZIP bundle locally

```bash
bash scripts/create_download_bundle.sh
```

This generates:

- `dist/QuantAI-Trad-full-program.zip`

You can share that ZIP directly.

## Option 2: Run directly from source

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m dashboard.app
```

## What is included in the ZIP

- AI feature engineering and ensemble modeling modules
- Trading/risk/execution/position management modules
- SQLite persistence layer and schemas
- PyQt6 desktop GUI dashboard
- Unit tests
- Packaging script for repeatable bundle creation
