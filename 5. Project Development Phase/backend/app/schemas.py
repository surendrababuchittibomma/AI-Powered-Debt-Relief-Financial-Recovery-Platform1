from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal

# User schemas
class UserCreate(BaseModel):
    name: str = Field(..., max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


# Loan schemas
class LoanCreate(BaseModel):
    loan_type: str = Field(..., max_length=50)
    loan_amount: Decimal = Field(..., gt=0)
    outstanding_amount: Decimal = Field(..., ge=0)
    interest_rate: Decimal = Field(..., ge=0, le=100)
    due_date: date

class LoanResponse(BaseModel):
    loan_id: int
    user_id: int
    loan_type: str
    loan_amount: Decimal
    outstanding_amount: Decimal
    interest_rate: Decimal
    due_date: date

    model_config = ConfigDict(from_attributes=True)


# Financial Profile schemas
class FinancialProfileCreate(BaseModel):
    monthly_income: Decimal = Field(..., ge=0)
    monthly_expenses: Decimal = Field(..., ge=0)
    existing_debts: Decimal = Field(..., ge=0)

class FinancialProfileResponse(BaseModel):
    profile_id: int
    user_id: int
    monthly_income: Decimal
    monthly_expenses: Decimal
    existing_debts: Decimal
    financial_health_score: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# Settlement Record schemas
class SettlementRecordResponse(BaseModel):
    settlement_id: int
    user_id: int
    loan_id: int
    settlement_prediction: str
    recommended_amount: Decimal
    priority_level: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# AI History schemas
class AIHistoryResponse(BaseModel):
    history_id: int
    user_id: int
    negotiation_strategy: str
    settlement_letter: str
    ai_response: str
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)
