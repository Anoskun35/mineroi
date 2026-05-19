"""Pydantic models for MineROI."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CalcRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    gpu: str = Field(..., description="GPU model identifier (e.g. RTX_4090)")
    coin: str = Field(..., description="Cryptocurrency to mine (ETH, RVN, ERG, KAS, NONCE)")
    electricity_usd: float = Field(..., alias="electricity", description="Electricity cost $/kWh")
    hours: float = Field(..., description="Mining duration in hours")
    price_override: float | None = Field(None, alias="price", description="Manual coin price override in USD")
    gpu_count: int = Field(1, alias="count", description="Number of GPUs")


class CalcResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    gpu: str
    gpu_name: str
    coin: str
    hashrate_mhs: float
    gpu_count: int
    total_hashrate_mhs: float
    electricity_usd_per_hour: float
    electricity_usd_total: float
    hours: float
    coin_price_usd: float
    coins_mined: float
    revenue_usd: float
    profit_usd: float
    roi_pct: float
    break_even_hours: float | None
    tdp_watts: int
    msrp_usd: int


class GPUInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    model: str
    name: str
    tdp_watts: int
    msrp_usd: int
    vram_gb: int
    hashrates: dict[str, float]


class CoinInfo(BaseModel):
    symbol: str
    name: str
    algorithm: str
