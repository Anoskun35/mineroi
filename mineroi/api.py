"""FastAPI REST API for MineROI."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from mineroi import __version__
from mineroi.calculator import calculate_roi
from mineroi.gpu_data import GPU_DATABASE, SUPPORTED_COINS, list_gpu_names
from mineroi.models import CalcRequest, CalcResult, GPUInfo
from mineroi.price_fetcher import COIN_NAMES, get_price

app = FastAPI(
    title="MineROI",
    description="GPU Mining Profitability Calculator",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.get("/api/v1/gpus")
def list_gpus() -> list[GPUInfo]:
    return [
        GPUInfo(
            model=model,
            name=gpu.name,
            tdp_watts=gpu.tdp_watts,
            msrp_usd=gpu.msrp_usd,
            vram_gb=gpu.vram_gb,
            hashrates=gpu.hashrates,
        )
        for model, gpu in sorted(GPU_DATABASE.items())
    ]


@app.get("/api/v1/coins")
def list_coins() -> list[dict]:
    return [
        {
            "symbol": coin,
            "name": COIN_NAMES.get(coin, coin),
            "price_usd": get_price(coin),
        }
        for coin in SUPPORTED_COINS
    ]


@app.post("/api/v1/calculate", response_model=CalcResult)
def calculate(req: CalcRequest) -> CalcResult:
    try:
        return calculate_roi(
            gpu_model=req.gpu,
            coin=req.coin.upper(),
            electricity_usd=req.electricity_usd,
            hours=req.hours,
            price_override=req.price_override,
            gpu_count=req.gpu_count,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
