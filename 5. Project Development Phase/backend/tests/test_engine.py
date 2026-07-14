from decimal import Decimal
from datetime import date, timedelta
from app.engine.financial import calculate_health_score
from app.engine.prediction import evaluate_settlement
from app.engine.advisor import generate_negotiation_package

def test_financial_health_score():
    # Good scenario: High savings, low debt
    score_good = calculate_health_score(
        income=Decimal("5000.00"),
        expenses=Decimal("1500.00"),
        debts=Decimal("200.00")
    )
    assert score_good > 70
    assert score_good <= 100

    # Bad scenario: Low savings, deficit, high debt
    score_bad = calculate_health_score(
        income=Decimal("3000.00"),
        expenses=Decimal("2500.00"),
        debts=Decimal("1000.00")
    )
    assert score_bad < 40

    # Zero income scenario
    score_zero = calculate_health_score(
        income=Decimal("0.00"),
        expenses=Decimal("1000.00"),
        debts=Decimal("500.00")
    )
    assert score_zero == 10


def test_settlement_evaluation():
    # delinquent and high interest
    outstanding = Decimal("12000.00")
    apr = Decimal("18.5")
    past_due_date = date.today() - timedelta(days=5)
    
    eval_critical = evaluate_settlement(
        outstanding_amount=outstanding,
        interest_rate=apr,
        due_date=past_due_date,
        financial_health_score=30
    )
    
    assert eval_critical["priority_level"] == "Critical"
    assert eval_critical["settlement_prediction"] == "High Probability"
    assert eval_critical["recommended_amount"] == outstanding * Decimal("0.40")

    # good financial standing
    eval_low_prob = evaluate_settlement(
        outstanding_amount=Decimal("1500.00"),
        interest_rate=Decimal("4.00"),
        due_date=date.today() + timedelta(days=90),
        financial_health_score=85
    )
    
    assert eval_low_prob["priority_level"] == "Normal"
    assert eval_low_prob["settlement_prediction"] == "Low Probability"
    assert eval_low_prob["recommended_amount"] == Decimal("1500.00") * Decimal("0.70")


def test_ai_advisor_fallback():
    package = generate_negotiation_package(
        borrower_name="John Doe",
        email="john@example.com",
        loan_type="Credit Card",
        outstanding_amount=Decimal("5000.00"),
        interest_rate=Decimal("15.00"),
        recommended_amount=Decimal("2000.00"),
        financial_health_score=50
    )
    
    assert "John Doe" in package["settlement_letter"]
    assert "$5,000.00" in package["settlement_letter"]
    assert "$2,000.00" in package["settlement_letter"]
    assert "john@example.com" in package["settlement_letter"]
    assert "Template Engine Fallback" in package["ai_response"] or "Gemini API" in package["ai_response"]
