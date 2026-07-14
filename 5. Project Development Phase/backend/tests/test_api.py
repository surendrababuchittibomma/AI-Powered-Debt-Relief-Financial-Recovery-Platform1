import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
import os

from app.database import Base, get_db
from app.main import app
from app import models

# Use a local test database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_finrelief.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    # Setup: Create tables
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    # Teardown: Drop tables and clean up file
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_finrelief.db"):
        try:
            os.remove("./test_finrelief.db")
        except Exception:
            pass

@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_auth_flow(client):
    # 1. Register a new user
    reg_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "securepassword"
    }
    response = client.post("/api/auth/register", json=reg_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "jane@example.com"
    assert "user_id" in data

    # 2. Register same user again should fail
    response = client.post("/api/auth/register", json=reg_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

    # 3. Login
    login_data = {
        "email": "jane@example.com",
        "password": "securepassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_financial_profile(client):
    # Login to get token
    login_data = {"email": "jane@example.com", "password": "securepassword"}
    token = client.post("/api/auth/login", json=login_data).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Get profile before creating should fail with 404
    response = client.get("/api/profile", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Financial profile not found. Please create one."

    # 2. Create profile
    profile_data = {
        "monthly_income": 6000.00,
        "monthly_expenses": 2000.00,
        "existing_debts": 400.00
    }
    response = client.post("/api/profile", json=profile_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert float(data["monthly_income"]) == 6000.00
    assert data["financial_health_score"] is not None
    # Expected health score: 80 - 10 (expense ratio > 0.2) - 10 (debt ratio > 0.0) + 20 (surplus ratio > 0.2) = 80
    assert data["financial_health_score"] >= 80

    # 3. Get profile now
    response = client.get("/api/profile", headers=headers)
    assert response.status_code == 200
    assert float(response.json()["monthly_income"]) == 6000.00


def test_loans_and_settlement_prediction(client):
    # Login to get token
    login_data = {"email": "jane@example.com", "password": "securepassword"}
    token = client.post("/api/auth/login", json=login_data).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Add a loan
    loan_date = (date.today() + timedelta(days=15)).strftime("%Y-%m-%d")
    loan_data = {
        "loan_type": "Personal Loan",
        "loan_amount": 5000.00,
        "outstanding_amount": 4000.00,
        "interest_rate": 12.50,
        "due_date": loan_date
    }
    response = client.post("/api/loans", json=loan_data, headers=headers)
    assert response.status_code == 201
    loan = response.json()
    assert loan["loan_type"] == "Personal Loan"
    assert float(loan["outstanding_amount"]) == 4000.00
    loan_id = loan["loan_id"]

    # 2. Get loans
    response = client.get("/api/loans", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # 3. Evaluate settlement
    response = client.post(f"/api/settlements/evaluate/{loan_id}", headers=headers)
    assert response.status_code == 200
    settlement = response.json()
    assert settlement["loan_id"] == loan_id
    assert "settlement_prediction" in settlement
    assert "recommended_amount" in settlement
    assert "priority_level" in settlement

    # 4. Get settlements history
    response = client.get("/api/settlements", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # 5. Generate AI Negotiation
    response = client.post(f"/api/negotiate/{loan_id}", headers=headers)
    assert response.status_code == 200
    negotiation = response.json()
    assert "negotiation_strategy" in negotiation
    assert "settlement_letter" in negotiation
    assert "ai_response" in negotiation

    # 6. Get negotiation history
    response = client.get("/api/negotiations", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # 7. Delete loan
    response = client.delete(f"/api/loans/{loan_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Loan record successfully deleted"

    # 8. Check loans empty
    response = client.get("/api/loans", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0
