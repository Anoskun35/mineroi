"""Typer CLI for MineROI."""

from __future__ import annotations

import json
import sys

import typer

from mineroi import __version__
from mineroi.calculator import calculate_roi
from mineroi.gpu_data import GPU_DATABASE, SUPPORTED_COINS, list_gpu_names
from mineroi.price_fetcher import get_price

app = typer.Typer(name="mineroi", help="GPU Mining Profitability Calculator")


@app.command()
def calc(
    gpu: str = typer.Option(..., help="GPU model (e.g. RTX_4090)"),
    coin: str = typer.Option(..., help="Coin to mine (ETH, RVN, ERG, KAS, NONCE)"),
    electricity: float = typer.Option(..., help="Electricity cost $/kWh"),
    hours: float = typer.Option(..., help="Mining duration in hours"),
    price: float = typer.Option(None, help="Manual coin price override (USD)"),
    count: int = typer.Option(1, help="Number of GPUs"),
    format: str = typer.Option("table", help="Output format: table, json, csv"),
) -> None:
    """Calculate mining profitability for a GPU."""
    try:
        result = calculate_roi(
            gpu_model=gpu,
            coin=coin.upper(),
            electricity_usd=electricity,
            hours=hours,
            price_override=price,
            gpu_count=count,
        )
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    if format == "json":
        typer.echo(json.dumps(result.model_dump(), indent=2))
    elif format == "csv":
        typer.echo("field,value")
        for k, v in result.model_dump().items():
            typer.echo(f"{k},{v}")
    else:
        _print_table(result)


@app.command(name="list-gpus")
def list_gpus_cmd() -> None:
    """List all supported GPUs with specs."""
    for model in list_gpu_names():
        gpu = GPU_DATABASE[model]
        coins = ", ".join(f"{c}:{h}" for c, h in gpu.hashrates.items() if h > 0)
        typer.echo(f"  {model:<15} {gpu.name:<25} TDP:{gpu.tdp_watts}W  VRAM:{gpu.vram_gb}GB  {coins}")


@app.command(name="list-coins")
def list_coins_cmd() -> None:
    """List all supported coins with current prices."""
    for coin in SUPPORTED_COINS:
        price = get_price(coin)
        typer.echo(f"  {coin:<8} ${price:.4f}")


@app.command(name="price")
def price_cmd(
    coin: str = typer.Option(..., help="Coin symbol"),
) -> None:
    """Fetch current price for a coin."""
    price = get_price(coin.upper())
    typer.echo(f"{coin.upper()}: ${price:.4f}")


def _print_table(result: object) -> None:
    d = result.model_dump() if hasattr(result, "model_dump") else result
    typer.echo("")
    typer.echo(f"  MineROI — {d['gpu_name']}")
    typer.echo(f"  {'=' * 50}")
    typer.echo(f"  GPU:              {d['gpu']} x{d['gpu_count']}")
    typer.echo(f"  Coin:             {d['coin']}")
    typer.echo(f"  Hashrate:         {d['total_hashrate_mhs']:.2f} MH/s")
    typer.echo(f"  Coin Price:       ${d['coin_price_usd']:.4f}")
    typer.echo(f"  Duration:         {d['hours']:.1f} hours")
    typer.echo(f"  {'─' * 50}")
    typer.echo(f"  Coins Mined:      {d['coins_mined']:.8f}")
    typer.echo(f"  Revenue:          ${d['revenue_usd']:.4f}")
    typer.echo(f"  Electricity:      ${d['electricity_usd_total']:.4f}")
    typer.echo(f"  Profit/Loss:      ${d['profit_usd']:.4f}")
    typer.echo(f"  ROI:              {d['roi_pct']:.1f}%")
    be = d.get("break_even_hours")
    typer.echo(f"  Break-even:       {f'{be:.1f}h' if be else 'Never'}")
    typer.echo(f"  {'─' * 50}")
    typer.echo(f"  TDP: {d['tdp_watts']}W  |  MSRP: ${d['msrp_usd']}")
    typer.echo("")


if __name__ == "__main__":
    app()
