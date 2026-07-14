from sqlalchemy.orm import Session
from . import models, schemas, security
from datetime import date
from decimal import Decimal

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pwd = security.get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Loan CRUD
def get_loans_by_user(db: Session, user_id: int):
    return db.query(models.Loan).filter(models.Loan.user_id == user_id).all()

def get_loan(db: Session, loan_id: int):
    return db.query(models.Loan).filter(models.Loan.loan_id == loan_id).first()

def create_loan(db: Session, loan: schemas.LoanCreate, user_id: int):
    db_loan = models.Loan(
        user_id=user_id,
        loan_type=loan.loan_type,
        loan_amount=loan.loan_amount,
        outstanding_amount=loan.outstanding_amount,
        interest_rate=loan.interest_rate,
        due_date=loan.due_date
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def delete_loan(db: Session, loan_id: int):
    db_loan = db.query(models.Loan).filter(models.Loan.loan_id == loan_id).first()
    if db_loan:
        db.delete(db_loan)
        db.commit()
        return True
    return False


# Financial Profile CRUD
def get_financial_profile(db: Session, user_id: int):
    return db.query(models.FinancialProfile).filter(models.FinancialProfile.user_id == user_id).first()

def create_or_update_financial_profile(db: Session, profile: schemas.FinancialProfileCreate, user_id: int, health_score: int):
    db_profile = db.query(models.FinancialProfile).filter(models.FinancialProfile.user_id == user_id).first()
    if db_profile:
        db_profile.monthly_income = profile.monthly_income
        db_profile.monthly_expenses = profile.monthly_expenses
        db_profile.existing_debts = profile.existing_debts
        db_profile.financial_health_score = health_score
    else:
        db_profile = models.FinancialProfile(
            user_id=user_id,
            monthly_income=profile.monthly_income,
            monthly_expenses=profile.monthly_expenses,
            existing_debts=profile.existing_debts,
            financial_health_score=health_score
        )
        db.add(db_profile)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile


# Settlement Record CRUD
def get_settlements_by_user(db: Session, user_id: int):
    return db.query(models.SettlementRecord).filter(models.SettlementRecord.user_id == user_id).all()

def create_settlement_record(
    db: Session,
    user_id: int,
    loan_id: int,
    prediction: str,
    recommended: Decimal,
    priority: str
):
    db_settlement = models.SettlementRecord(
        user_id=user_id,
        loan_id=loan_id,
        settlement_prediction=prediction,
        recommended_amount=recommended,
        priority_level=priority
    )
    db.add(db_settlement)
    db.commit()
    db.refresh(db_settlement)
    return db_settlement


# AI History CRUD
def get_ai_histories_by_user(db: Session, user_id: int):
    return db.query(models.AIHistory).filter(models.AIHistory.user_id == user_id).all()

def create_ai_history_record(
    db: Session,
    user_id: int,
    strategy: str,
    letter: str,
    ai_response: str
):
    db_history = models.AIHistory(
        user_id=user_id,
        negotiation_strategy=strategy,
        settlement_letter=letter,
        ai_response=ai_response
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history
