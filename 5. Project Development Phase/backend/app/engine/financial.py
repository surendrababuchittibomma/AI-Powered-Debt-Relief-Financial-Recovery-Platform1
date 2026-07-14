from decimal import Decimal

def calculate_health_score(income: Decimal, expenses: Decimal, debts: Decimal) -> int:
    """
    Calculates a financial health score from 0 to 100 based on income, expenses, and existing debts.
    Formula balances expenses-to-income ratio, debt-to-income ratio, and net monthly surplus.
    """
    if income <= 0:
        return 10  # Minimum base score if no income is recorded.

    # 1. Expenses to Income Ratio (Deductions up to 40 points)
    expense_ratio = float(expenses / income)
    expense_penalty = 0
    if expense_ratio > 0.8:
        expense_penalty = 40
    elif expense_ratio > 0.6:
        expense_penalty = 30
    elif expense_ratio > 0.4:
        expense_penalty = 20
    elif expense_ratio > 0.2:
        expense_penalty = 10

    # 2. Debt to Income Ratio (Deductions up to 40 points)
    debt_ratio = float(debts / income)
    debt_penalty = 0
    if debt_ratio > 0.6:
        debt_penalty = 40
    elif debt_ratio > 0.4:
        debt_penalty = 30
    elif debt_ratio > 0.2:
        debt_penalty = 20
    elif debt_ratio > 0.1:
        debt_penalty = 10

    # 3. Surplus Ratio (Up to 20 bonus points, starts from base score of 80)
    surplus = income - expenses - debts
    surplus_ratio = float(surplus / income)
    
    score = 80 - expense_penalty - debt_penalty
    
    if surplus_ratio > 0.2:
        score += 20
    elif surplus_ratio > 0.1:
        score += 10
    elif surplus_ratio < 0:
        # Penalize further for deficit budget
        score -= 15

    # Ensure score is strictly bounded between 0 and 100
    return max(0, min(100, int(score)))
