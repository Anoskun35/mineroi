"""Core mining profitability calculator."""

from __future__ import annotations

from mineroi.gpu_data import get_gpu
from mineroi.models import CalcResult
from mineroi.price_fetcher import get_price


def calculate_roi(
    gpu_model: str,
    coin: str,
    electricity_usd: float,
    hours: float,
    price_override: float | None = None,
    gpu_count: int = 1,
) -> CalcResult:
    """Calculate mining ROI for a given GPU and coin."""

    gpu = get_gpu(gpu_model)
    if gpu is None:
        raise ValueError(f"Unknown GPU: {gpu_model}. Use list-gpus to see options.")

    hashrate = gpu.hashrate(coin)
    if hashrate <= 0:
        raise ValueError(f"{gpu.name} does not support {coin} mining.")

    # Price
    coin_price = price_override if price_override and price_override > 0 else get_price(coin)

    # Electricity
    elec_per_hour = (gpu.tdp_watts * gpu_count / 1000) * electricity_usd
    elec_total = elec_per_hour * hours

    # Mining output
    total_hashrate = hashrate * gpu_count
    # Coins mined = hashrate(MH/s) * hours * 3600s / network_difficulty_factor
    # Simplified: use hashrate as proxy for coins/hour based on empirical data
    coins_per_hour = total_hashrate * _mining_factor(coin)
    coins_mined = coins_per_hour * hours

    # Revenue & profit
    revenue = coins_mined * coin_price
    profit = revenue - elec_total
    roi_pct = (profit / elec_total * 100) if elec_total > 0 else 0.0

    # Break-even
    break_even = None
    revenue_per_hour = coins_per_hour * coin_price
    if revenue_per_hour > elec_per_hour:
        break_even = elec_total / (revenue_per_hour - elec_per_hour) if (revenue_per_hour - elec_per_hour) > 0 else None
    elif revenue_per_hour > 0:
        # Never breaks even, calculate how many hours to lose all investment
        break_even = None

    return CalcResult(
        gpu=gpu_model,
        gpu_name=gpu.name,
        coin=coin,
        hashrate_mhs=hashrate,
        gpu_count=gpu_count,
        total_hashrate_mhs=total_hashrate,
        electricity_usd_per_hour=round(elec_per_hour, 6),
        electricity_usd_total=round(elec_total, 4),
        hours=hours,
        coin_price_usd=coin_price,
        coins_mined=round(coins_mined, 8),
        revenue_usd=round(revenue, 4),
        profit_usd=round(profit, 4),
        roi_pct=round(roi_pct, 2),
        break_even_hours=round(break_even, 1) if break_even else None,
        tdp_watts=gpu.tdp_watts,
        msrp_usd=gpu.msrp_usd,
    )


def _mining_factor(coin: str) -> float:
    """Coins per MH/s per hour — empirical estimates."""
    factors = {
        "ETH": 0.000032,
        "RVN": 0.45,
        "ERG": 0.015,
        "KAS": 0.08,
        "NONCE": 95.0,
    }
    return factors.get(coin, 0.0)
