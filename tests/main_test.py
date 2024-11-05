import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_database_url
from database import Base
from main import app, get_db

# Use PostgreSQL for testing
SQLALCHEMY_DATABASE_URL = get_database_url()

# Create a test database engine with PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)


# Override the get_db dependency for testing
def override_get_db():
    """
    Dependency override for database session in tests.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(autouse=True)
def run_around_tests():
    """
    Runs before each test. Clears data from the database.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user():
    """
    Test creating a new user.
    """
    response = client.post(
        "/users",
        json={
            "firstname": "Alice",
            "lastname": "Smith",
            "age": 28,
            "date_of_birth": "1995-02-20",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["firstname"] == "Alice"
    assert data["lastname"] == "Smith"
    assert data["age"] == 28
    assert data["date_of_birth"] == "1995-02-20"
    assert "id" in data


def test_create_user_missing_fields():
    """
    Test creating a user with missing required fields.
    Should return a 422 Unprocessable Entity error.
    """
    response = client.post(
        "/users",
        json={
            "firstname": "Bob",
            # "lastname" is missing
            "age": 25,
            "date_of_birth": "1998-03-15",
        },
    )
    assert response.status_code == 422
    data = response.json()
    assert any(
        error["loc"] == ["body", "lastname"] and error["msg"] == "Field required"
        for error in data["detail"]
    )


def test_create_user_invalid_age():
    """
    Test creating a user with invalid age (negative number).
    Should return a 422 Unprocessable Entity error.
    """
    response = client.post(
        "/users",
        json={
            "firstname": "Charlie",
            "lastname": "Brown",
            "age": -5,  # Invalid age
            "date_of_birth": "2000-05-10",
        },
    )
    assert response.status_code == 422
    data = response.json()
    
    assert any(
        error["loc"] == ["body", "age"]
        and "Input should be greater than or equal to 0" in error["msg"]
        for error in data["detail"]
    )


def test_get_users():
    """
    Test retrieving all users.
    """
    # Create a user first
    test_create_user()
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["firstname"] == "Alice"