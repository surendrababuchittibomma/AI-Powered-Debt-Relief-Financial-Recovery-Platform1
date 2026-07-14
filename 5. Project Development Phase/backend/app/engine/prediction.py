from decimal import Decimal
from datetime import date

def evaluate_settlement(
    outstanding_amount: Decimal,
    interest_rate: Decimal,
    due_date: date,
    financial_health_score: int
) -> dict:
    """
    Evaluates settlement probability, recommended settlement payoff amount, and priority level.
    Uses rule-based heuristics incorporating outstanding debt balance, interest rate, and financial capacity.
    """
    # 1. Evaluate Priority Level
    # Higher interest rates and larger balances warrant higher priorities
    priority_score = 0
    if interest_rate > 15:
        priority_score += 4
    elif interest_rate > 8:
        priority_score += 2

    if outstanding_amount > 10000:
        priority_score += 4
    elif outstanding_amount > 3000:
        priority_score += 2

    # If due date is already passed or near, increase priority
    days_to_due = (due_date - date.today()).days
    if days_to_due < 0:
        priority_score += 4  # Past due
    elif days_to_due < 30:
        priority_score += 2  # Approaching maturity

    if priority_score >= 8:
        priority_level = "Critical"
    elif priority_score >= 4:
        priority_level = "High"
    else:
        priority_level = "Normal"

    # 2. Evaluate Settlement Prediction (Probability of Acceptance)
    # Creditors are more willing to settle if the debtor's financial score is low (high default risk)
    if financial_health_score < 40:
        settlement_prediction = "High Probability"
        discount_factor = Decimal("0.40")  # Settle for 40% of outstanding balance
    elif financial_health_score < 70:
        settlement_prediction = "Medium Probability"
        discount_factor = Decimal("0.55")  # Settle for 55% of outstanding balance
    else:
        settlement_prediction = "Low Probability"
        discount_factor = Decimal("0.70")  # Settle for 70% of outstanding balance

    recommended_amount = outstanding_amount * discount_factor

    return {
        "settlement_prediction": settlement_prediction,
        "recommended_amount": recommended_amount.quantize(Decimal("0.01")),
        "priority_level": priority_level
    }
