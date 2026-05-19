"""Tests for FastAPI REST API."""

import os
os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

import pytest
from fastapi.testclient import TestClient
from mineroi.api import app

client = TestClient(app)


class TestHealth:
    def test_health(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


class TestGPUs:
    def test_list_gpus(self):
        resp = client.get("/api/v1/gpus")
        assert resp.status_code == 200
        gpus = resp.json()
        assert len(gpus) >= 15
        assert any(g["model"] == "RTX_4090" for g in gpus)

    def test_gpu_has_hashrates(self):
        resp = client.get("/api/v1/gpus")
        for gpu in resp.json():
            assert "hashrates" in gpu
            assert "ETH" in gpu["hashrates"]


class TestCoins:
    def test_list_coins(self):
        resp = client.get("/api/v1/coins")
        assert resp.status_code == 200
        coins = resp.json()
        symbols = [c["symbol"] for c in coins]
        assert "ETH" in symbols
        assert "NONCE" in symbols


class TestCalculate:
    def test_calculate_success(self):
        resp = client.post("/api/v1/calculate", json={
            "gpu": "RTX_4090",
            "coin": "ETH",
            "electricity": 0.10,
            "hours": 24,
            "price": 2000.0,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["gpu"] == "RTX_4090"
        assert data["coin"] == "ETH"
        assert data["revenue_usd"] > 0

    def test_calculate_bad_gpu(self):
        resp = client.post("/api/v1/calculate", json={
            "gpu": "RTX_9999",
            "coin": "ETH",
            "electricity": 0.10,
            "hours": 24,
        })
        assert resp.status_code == 400

    def test_calculate_bad_coin(self):
        resp = client.post("/api/v1/calculate", json={
            "gpu": "RTX_4090",
            "coin": "BTC",
            "electricity": 0.10,
            "hours": 24,
        })
        assert resp.status_code == 400

    def test_calculate_with_count(self):
        resp = client.post("/api/v1/calculate", json={
            "gpu": "RTX_4090",
            "coin": "ETH",
            "electricity": 0.10,
            "hours": 24,
            "price": 2000.0,
            "count": 4,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["gpu_count"] == 4
