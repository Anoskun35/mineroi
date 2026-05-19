"""Tests for Pydantic models."""

import os
os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

import pytest
from mineroi.models import CalcRequest, CalcResult, GPUInfo, CoinInfo


class TestModels:
    def test_calc_request(self):
        req = CalcRequest(gpu="RTX_4090", coin="ETH", electricity=0.10, hours=24)
        assert req.gpu == "RTX_4090"
        assert req.electricity_usd == 0.10
        assert req.gpu_count == 1  # default

    def test_calc_request_with_count(self):
        req = CalcRequest(gpu="RTX_4090", coin="ETH", electricity=0.10, hours=24, count=4)
        assert req.gpu_count == 4

    def test_calc_result(self):
        result = CalcResult(
            gpu="RTX_4090", gpu_name="NVIDIA RTX 4090", coin="ETH",
            hashrate_mhs=130.0, gpu_count=1, total_hashrate_mhs=130.0,
            electricity_usd_per_hour=0.045, electricity_usd_total=1.08,
            hours=24, coin_price_usd=2000.0, coins_mined=0.10,
            revenue_usd=200.0, profit_usd=198.92, roi_pct=18418.5,
            break_even_hours=0.024, tdp_watts=450, msrp_usd=1599,
        )
        assert result.gpu == "RTX_4090"
        assert result.profit_usd == 198.92

    def test_gpu_info(self):
        info = GPUInfo(
            model="RTX_4090", name="NVIDIA RTX 4090",
            tdp_watts=450, msrp_usd=1599, vram_gb=24,
            hashrates={"ETH": 130.0},
        )
        assert info.model == "RTX_4090"

    def test_coin_info(self):
        info = CoinInfo(symbol="ETH", name="Ethereum", algorithm="Ethash")
        assert info.symbol == "ETH"
