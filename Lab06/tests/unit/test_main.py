from pathlib import Path
import pytest
from reliable_finance.main import main


def test_main_missing_config(monkeypatch, tmp_path: Path):
    # Підміняємо робочу директорію або шлях, щоб config.yaml не знайшло
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1