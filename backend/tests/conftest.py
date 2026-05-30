import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.db_models import Base
from app.db.session import get_db
from app.services.sentiment import SentimentService

# ── In-memory SQLite DB for tests ────────────────────────────────────────────
SQLITE_URL = "sqlite:///./test_sentivex.db"
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    session = TestingSession()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture()
def mock_service() -> SentimentService:
    service = MagicMock(spec=SentimentService)
    service.model_loaded = True
    service.predict.return_value = {
        "sentiment": "Positive",
        "confidence": 0.95,
        "scores": {"positive": 0.95, "neutral": 0.03, "negative": 0.02},
        "cleaned_text": "great product",
    }
    service.predict_batch.return_value = [service.predict.return_value]
    return service


@pytest.fixture()
def client(db_session, mock_service):
    app.dependency_overrides[get_db] = lambda: db_session
    app.state.sentiment_service = mock_service
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
