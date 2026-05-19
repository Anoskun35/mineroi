# MineROI — GPU Mining Profitability Calculator

A production-quality GPU mining profitability calculator that helps crypto miners decide if mining is worth it.

## Features

- **15 GPU models** supported (NVIDIA RTX 30/40/50 series, AMD RX)
- **5 cryptocurrencies**: ETH, RVN, ERG, KAS, NONCE
- **Real-time prices** via CoinGecko API
- **CLI** (Typer) and **REST API** (FastAPI)
- **Export** results as JSON/CSV

## Quick Start

### CLI

```bash
pip install -e .

# Calculate profitability
mineroi calc --gpu RTX_4090 --coin ETH --electricity 0.10 --hours 24

# With manual price override
mineroi calc --gpu RTX_4090 --coin ETH --electricity 0.10 --hours 24 --price 2000

# List all GPUs
mineroi list-gpus

# Export as JSON
mineroi calc --gpu RTX_4090 --coin ETH --electricity 0.10 --hours 720 --format json

# Export as CSV
mineroi calc --gpu RTX_4090 --coin ETH --electricity 0.10 --hours 720 --format csv
```

### REST API

```bash
uvicorn mineroi.api:app --host 0.0.0.0 --port 8000
```

- `GET /api/v1/gpus` — list all GPUs
- `POST /api/v1/calculate` — calculate mining ROI
- `GET /api/v1/coins` — list supported coins
- `GET /health` — health check

## Project Structure

```
mineroi/
├── mineroi/
│   ├── __init__.py
│   ├── models.py        # Pydantic models
│   ├── cli.py           # Typer CLI
│   ├── api.py           # FastAPI REST
│   ├── calculator.py    # Core ROI logic
│   ├── gpu_data.py      # GPU specs database
│   └── price_fetcher.py # CoinGecko API
├── tests/
└── examples/
```

## License

MIT
