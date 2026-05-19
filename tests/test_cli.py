"""Tests for CLI commands."""

import os
os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

import pytest
from typer.testing import CliRunner
from mineroi.cli import app

runner = CliRunner()


class TestCLI:
    def test_calc_table(self):
        result = runner.invoke(app, [
            "calc", "--gpu", "RTX_4090", "--coin", "ETH",
            "--electricity", "0.10", "--hours", "24",
            "--price", "2000",
        ])
        assert result.exit_code == 0
        assert "RTX 4090" in result.output
        assert "Revenue" in result.output

    def test_calc_json(self):
        result = runner.invoke(app, [
            "calc", "--gpu", "RTX_4090", "--coin", "ETH",
            "--electricity", "0.10", "--hours", "24",
            "--price", "2000", "--format", "json",
        ])
        assert result.exit_code == 0
        assert '"gpu": "RTX_4090"' in result.output

    def test_calc_csv(self):
        result = runner.invoke(app, [
            "calc", "--gpu", "RTX_4090", "--coin", "ETH",
            "--electricity", "0.10", "--hours", "24",
            "--price", "2000", "--format", "csv",
        ])
        assert result.exit_code == 0
        assert "field,value" in result.output

    def test_calc_bad_gpu(self):
        result = runner.invoke(app, [
            "calc", "--gpu", "RTX_9999", "--coin", "ETH",
            "--electricity", "0.10", "--hours", "24",
        ])
        assert result.exit_code == 1

    def test_list_gpus(self):
        result = runner.invoke(app, ["list-gpus"])
        assert result.exit_code == 0
        assert "RTX_4090" in result.output
        assert "RTX_5090" in result.output

    def test_list_coins(self):
        result = runner.invoke(app, ["list-coins"])
        assert result.exit_code == 0
        assert "ETH" in result.output
