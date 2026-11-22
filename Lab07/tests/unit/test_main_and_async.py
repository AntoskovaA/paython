import asyncio
from pathlib import Path
import pytest
from unittest.mock import AsyncMock
from reliable_finance.main import main
from reliable_finance.logging_config import configure_logging


def test_main_missing_config(monkeypatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1


def test_configure_logging(tmp_path: Path):
    log_file = tmp_path / "logs" / "app.log"
    configure_logging("INFO", log_file)
    assert log_file.parent.exists()


def test_async_mock_usage():
    # Перевірка AsyncMock та await виконання
    async def run_async_test():
        client = AsyncMock()
        client.fetch_balance.return_value = 2500.0
        val = await client.fetch_balance()
        assert val == 2500.0
        client.fetch_balance.assert_awaited_once()

    asyncio.run(run_async_test())