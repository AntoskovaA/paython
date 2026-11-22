from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from collections.abc import Generator

from reliable_finance.db_models import Base


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Окрема тестова база SQLite у пам'яті для інтеграційних тестів persistence layer."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with TestSession() as session:
        yield session
    Base.metadata.drop_all(engine)


@pytest.fixture
def sqlite_db_file(tmp_path: Path) -> Path:
    """Окрема файлова тестова SQLite БД для перевірки запитів через DB-API."""
    db_path = tmp_path / "test_finance.db"
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)
    engine.dispose()
    return db_path