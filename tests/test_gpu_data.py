"""Tests for GPU data database."""

import os
os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

import pytest
from mineroi.gpu_data import GPU_DATABASE, SUPPORTED_COINS, get_gpu, list_gpus, list_gpu_names


class TestGPUData:
    def test_database_not_empty(self):
        assert len(GPU_DATABASE) >= 15

    def test_get_gpu_known(self):
        gpu = get_gpu("RTX_4090")
        assert gpu is not None
        assert gpu.name == "NVIDIA RTX 4090"
        assert gpu.tdp_watts == 450

    def test_get_gpu_unknown(self):
        assert get_gpu("RTX_9999") is None

    def test_list_gpus(self):
        gpus = list_gpus()
        assert len(gpus) >= 15

    def test_list_gpu_names(self):
        names = list_gpu_names()
        assert "RTX_4090" in names
        assert "RTX_5090" in names
        assert names == sorted(names)

    def test_all_gpus_have_positive_tdp(self):
        for gpu in list_gpus():
            assert gpu.tdp_watts > 0, f"{gpu.name} has zero TDP"

    def test_all_gpus_have_msrp(self):
        for gpu in list_gpus():
            assert gpu.msrp_usd > 0, f"{gpu.name} has zero MSRP"

    def test_hashrate_non_negative(self):
        for gpu in list_gpus():
            for coin in SUPPORTED_COINS:
                assert gpu.hashrate(coin) >= 0, f"{gpu.name} negative hashrate for {coin}"

    def test_supported_coins(self):
        assert len(SUPPORTED_COINS) == 5
        assert "ETH" in SUPPORTED_COINS
        assert "NONCE" in SUPPORTED_COINS
