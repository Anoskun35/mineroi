"""Tests for core calculator logic."""

import os
os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

import pytest
from mineroi.calculator import calculate_roi, _mining_factor
from mineroi.gpu_data import list_gpu_names


class TestCalculateROI:
    def test_basic_calculation(self):
        result = calculate_roi("RTX_4090", "ETH", 0.10, 24, price_override=2000.0)
        assert result.gpu == "RTX_4090"
        assert result.coin == "ETH"
        assert result.hours == 24
        assert result.coin_price_usd == 2000.0
        assert result.revenue_usd > 0
        assert result.electricity_usd_total > 0

    def test_profit_or_loss(self):
        result = calculate_roi("RTX_4090", "ETH", 0.10, 24, price_override=2000.0)
        assert isinstance(result.profit_usd, float)
        assert isinstance(result.roi_pct, float)

    def test_multi_gpu(self):
        r1 = calculate_roi("RTX_4090", "ETH", 0.10, 24, price_override=2000.0, gpu_count=1)
        r2 = calculate_roi("RTX_4090", "ETH", 0.10, 24, price_override=2000.0, gpu_count=2)
        assert r2.total_hashrate_mhs == r1.total_hashrate_mhs * 2
        assert r2.electricity_usd_total == pytest.approx(r1.electricity_usd_total * 2, rel=1e-4)
        assert r2.coins_mined == pytest.approx(r1.coins_mined * 2, rel=1e-4)

    def test_price_override(self):
        r1 = calculate_roi("RTX_4090", "ETH", 0.10, 24, price_override=1000.0)
        r2 = calculate_roi("RTX_4090", "ETH", 0.10, 24, price_override=3000.0)
        assert r2.revenue_usd > r1.revenue_usd
        assert r2.profit_usd > r1.profit_usd

    def test_electricity_cost_scales(self):
        r1 = calculate_roi("RTX_4090", "ETH", 0.05, 24, price_override=2000.0)
        r2 = calculate_roi("RTX_4090", "ETH", 0.20, 24, price_override=2000.0)
        assert r2.electricity_usd_total > r1.electricity_usd_total
        assert r2.profit_usd < r1.profit_usd

    def test_unknown_gpu_raises(self):
        with pytest.raises(ValueError, match="Unknown GPU"):
            calculate_roi("RTX_9999", "ETH", 0.10, 24)

    def test_unsupported_coin_raises(self):
        with pytest.raises(ValueError, match="does not support"):
            calculate_roi("RTX_4090", "BTC", 0.10, 24)

    def test_longer_duration_more_coins(self):
        r1 = calculate_roi("RTX_4090", "ETH", 0.10, 24, price_override=2000.0)
        r2 = calculate_roi("RTX_4090", "ETH", 0.10, 72, price_override=2000.0)
        assert r2.coins_mined == pytest.approx(r1.coins_mined * 3, rel=1e-4)

    def test_all_gpus_have_hashrates(self):
        for model in list_gpu_names():
            for coin in ["ETH", "RVN", "ERG", "KAS"]:
                result = calculate_roi(model, coin, 0.10, 1, price_override=1.0)
                assert result.hashrate_mhs > 0


class TestMiningFactor:
    def test_eth_factor(self):
        assert _mining_factor("ETH") > 0

    def test_nonce_factor(self):
        assert _mining_factor("CFX") > 0

    def test_unknown_coin_returns_zero(self):
        assert _mining_factor("DOGE") == 0.0
