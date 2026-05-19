"""CoinGecko price fetcher with fallback defaults."""

from __future__ import annotations

import httpx

COINGECKO_API = "https://api.coingecko.com/api/v3"

COIN_IDS = {
    "ETH": "ethereum",
    "RVN": "ravencoin",
    "ERG": "ergo",
    "KAS": "kaspa",
    "NONCE": "nonce-agent-8004",
}

DEFAULT_PRICES = {
    "ETH": 2100.0,
    "RVN": 0.03,
    "ERG": 1.50,
    "KAS": 0.12,
    "NONCE": 0.013,
}

COIN_NAMES = {
    "ETH": "Ethereum",
    "RVN": "Ravencoin",
    "ERG": "Ergo",
    "KAS": "Kaspa",
    "NONCE": "Nonce",
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
