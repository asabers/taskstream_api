import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app, get_db
from src.models import Base, User, Task # Explicitly import models to register them

# Connection string for isolated in-memory execution
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Engine initialization with thread-safety and pool configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """
    Handles the setup and teardown of the database schema.
    Provides a local session for individual test execution.
    """
    # Initialize schema before test run
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables to ensure a clean slate for the next test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """
    Provides a TestClient instance with injected database dependencies.
    Overrides the production database yield with the testing session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    # Map production dependency to the testing override
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c