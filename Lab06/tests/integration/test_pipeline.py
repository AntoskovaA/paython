from pathlib import Path
import json
import pytest
from reliable_finance.services import ImportStatistics, filter_by_minimum_amount, import_transactions
from reliable_finance.exporters import atomic_export_json


@pytest.mark.integration
def test_full_pipeline_integration(sample_config):
    stats = ImportStatistics()
    
    # 1. Імпорт
    stream = import_transactions(
        sample_config.input_path,
        skip_invalid=sample_config.processing.skip_invalid,
        allowed_categories=sample_config.processing.allowed_categories,
        statistics=stats
    )
    
    # 2. Фільтрація
    filtered = filter_by_minimum_amount(stream, sample_config.processing.minimum_amount)
    
    # 3. Атомарний експорт
    count = atomic_export_json(filtered, sample_config.output_path)
    
    assert count == 1
    assert sample_config.output_path.exists()
    
    data = json.loads(sample_config.output_path.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["category"] == "Зарплата"
    assert data[0]["amount"] == 15000.0