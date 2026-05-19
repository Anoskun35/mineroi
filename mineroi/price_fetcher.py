"""CoinGecko price fetcher with fallback defaults."""

from __future__ import annotations

import httpx

COINGECKO_API = "https://api.coingecko.com/api/v3"

COIN_IDS = {
    "ETH": "ethereum",
    "ETC": "ethereum-classic",
    "RVN": "ravencoin",
    "ERG": "ergo",
    "KAS": "kaspa",
    "CFX": "conflux-token",
    "ZEC": "zcash",
}

DEFAULT_PRICES = {
    "ETH": 2100.0,
    "ETC": 28.0,
    "RVN": 0.03,
    "ERG": 1.50,
    "KAS": 0.12,
    "CFX": 0.08,
    "ZEC": 28.0,
}

COIN_NAMES = {
    "ETH": "Ethereum",
    "ETC": "Ethereum Classic",
    "RVN": "Ravencoin",
    "ERG": "Ergo",
    "KAS": "Kaspa",
    "CFX": "Conflux",
    "ZEC": "Zcash",
}


def get_price(coin: str, timeout: float = 5.0) -> float:
    """Fetch current price from CoinGecko. Falls back to default on error."""
    cg_id = COIN_IDS.get(coin)
    if not cg_id:
        return DEFAULT_PRICES.get(coin, 0.0)

    try:
        resp = httpx.get(
            f"{COINGECKO_API}/simple/price",
            params={"ids": cg_id, "vs_currencies": "usd"},
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        return float(data[cg_id]["usd"])
    except Exception:
        return DEFAULT_PRICES.get(coin, 0.0)
