"""GPU specifications database — hashrate, TDP, MSRP for mining."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GPUSpec:
    name: str
    hashrates: dict[str, float]  # coin -> MH/s
    tdp_watts: int
    msrp_usd: int
    vram_gb: int

    def hashrate(self, coin: str) -> float:
        return self.hashrates.get(coin, 0.0)


# Hashrates in MH/s (or KH/s for ERG/KAS scaled to MH/s equivalent)
GPU_DATABASE: dict[str, GPUSpec] = {
    "RTX_3060": GPUSpec(
        name="NVIDIA RTX 3060",
        hashrates={"ETH": 48, "ETC": 48, "RVN": 22, "ERG": 62, "KAS": 42, "CFX": 46, "ZEC": 44},
        tdp_watts=170, msrp_usd=329, vram_gb=12,
    ),
    "RTX_3070": GPUSpec(
        name="NVIDIA RTX 3070",
        hashrates={"ETH": 62, "ETC": 62, "RVN": 30, "ERG": 83, "KAS": 58, "CFX": 60, "ZEC": 58},
        tdp_watts=220, msrp_usd=499, vram_gb=8,
    ),
    "RTX_3080": GPUSpec(
        name="NVIDIA RTX 3080",
        hashrates={"ETH": 100, "ETC": 100, "RVN": 45, "ERG": 130, "KAS": 87, "CFX": 96, "ZEC": 95},
        tdp_watts=320, msrp_usd=699, vram_gb=10,
    ),
    "RTX_3090": GPUSpec(
        name="NVIDIA RTX 3090",
        hashrates={"ETH": 120, "ETC": 120, "RVN": 55, "ERG": 155, "KAS": 105, "CFX": 115, "ZEC": 110},
        tdp_watts=350, msrp_usd=1499, vram_gb=24,
    ),
    "RTX_4060": GPUSpec(
        name="NVIDIA RTX 4060",
        hashrates={"ETH": 35, "ETC": 35, "RVN": 18, "ERG": 52, "KAS": 38, "CFX": 33, "ZEC": 32},
        tdp_watts=115, msrp_usd=299, vram_gb=8,
    ),
    "RTX_4060_Ti": GPUSpec(
        name="NVIDIA RTX 4060 Ti",
        hashrates={"ETH": 50, "ETC": 50, "RVN": 25, "ERG": 72, "KAS": 52, "CFX": 48, "ZEC": 46},
        tdp_watts=160, msrp_usd=399, vram_gb=8,
    ),
    "RTX_4070": GPUSpec(
        name="NVIDIA RTX 4070",
        hashrates={"ETH": 65, "ETC": 65, "RVN": 32, "ERG": 88, "KAS": 62, "CFX": 62, "ZEC": 60},
        tdp_watts=200, msrp_usd=599, vram_gb=12,
    ),
    "RTX_4070_Ti": GPUSpec(
        name="NVIDIA RTX 4070 Ti",
        hashrates={"ETH": 80, "ETC": 80, "RVN": 38, "ERG": 105, "KAS": 75, "CFX": 77, "ZEC": 74},
        tdp_watts=285, msrp_usd=799, vram_gb=12,
    ),
    "RTX_4080": GPUSpec(
        name="NVIDIA RTX 4080",
        hashrates={"ETH": 105, "ETC": 105, "RVN": 48, "ERG": 140, "KAS": 95, "CFX": 100, "ZEC": 98},
        tdp_watts=320, msrp_usd=1199, vram_gb=16,
    ),
    "RTX_4090": GPUSpec(
        name="NVIDIA RTX 4090",
        hashrates={"ETH": 130, "ETC": 130, "RVN": 60, "ERG": 170, "KAS": 120, "CFX": 125, "ZEC": 122},
        tdp_watts=450, msrp_usd=1599, vram_gb=24,
    ),
    "RTX_5060": GPUSpec(
        name="NVIDIA RTX 5060",
        hashrates={"ETH": 55, "ETC": 55, "RVN": 28, "ERG": 78, "KAS": 55, "CFX": 52, "ZEC": 50},
        tdp_watts=145, msrp_usd=299, vram_gb=8,
    ),
    "RTX_5060_Ti": GPUSpec(
        name="NVIDIA RTX 5060 Ti",
        hashrates={"ETH": 70, "ETC": 70, "RVN": 35, "ERG": 95, "KAS": 68, "CFX": 67, "ZEC": 65},
        tdp_watts=180, msrp_usd=449, vram_gb=16,
    ),
    "RTX_5070": GPUSpec(
        name="NVIDIA RTX 5070",
        hashrates={"ETH": 90, "ETC": 90, "RVN": 42, "ERG": 120, "KAS": 85, "CFX": 86, "ZEC": 83},
        tdp_watts=250, msrp_usd=549, vram_gb=12,
    ),
    "RTX_5070_Ti": GPUSpec(
        name="NVIDIA RTX 5070 Ti",
        hashrates={"ETH": 115, "ETC": 115, "RVN": 52, "ERG": 155, "KAS": 110, "CFX": 110, "ZEC": 107},
        tdp_watts=300, msrp_usd=749, vram_gb=16,
    ),
    "RTX_5090": GPUSpec(
        name="NVIDIA RTX 5090",
        hashrates={"ETH": 180, "ETC": 180, "RVN": 80, "ERG": 220, "KAS": 160, "CFX": 172, "ZEC": 168},
        tdp_watts=575, msrp_usd=1999, vram_gb=32,
    ),
    "RX_6800_XT": GPUSpec(
        name="AMD RX 6800 XT",
        hashrates={"ETH": 64, "ETC": 64, "RVN": 32, "ERG": 110, "KAS": 65, "CFX": 62, "ZEC": 58},
        tdp_watts=300, msrp_usd=649, vram_gb=16,
    ),
    "RX_7900_XTX": GPUSpec(
        name="AMD RX 7900 XTX",
        hashrates={"ETH": 80, "ETC": 80, "RVN": 45, "ERG": 150, "KAS": 95, "CFX": 77, "ZEC": 72},
        tdp_watts=355, msrp_usd=999, vram_gb=24,
    ),
}

SUPPORTED_COINS = ["ETH", "ETC", "RVN", "ERG", "KAS", "CFX", "ZEC"]


def get_gpu(model: str) -> GPUSpec | None:
    return GPU_DATABASE.get(model)


def list_gpus() -> list[GPUSpec]:
    return list(GPU_DATABASE.values())


def list_gpu_names() -> list[str]:
    return sorted(GPU_DATABASE.keys())
