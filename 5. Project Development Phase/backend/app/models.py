from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    loans = relationship("Loan", back_populates="borrower", cascade="all, delete-orphan")
    financial_profile = relationship("FinancialProfile", uselist=False, back_populates="borrower", cascade="all, delete-orphan")
    settlement_records = relationship("SettlementRecord", back_populates="borrower", cascade="all, delete-orphan")
    ai_histories = relationship("AIHistory", back_populates="borrower", cascade="all, delete-orphan")


class Loan(Base):
    __tablename__ = "loans"

    loan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    loan_type = Column(String(50), nullable=False)
    loan_amount = Column(Numeric(15, 2), nullable=False)
    outstanding_amount = Column(Numeric(15, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), nullable=False)
    due_date = Column(Date, nullable=False)

    # Relationships
    borrower = relationship("User", back_populates="loans")
    settlement_records = relationship("SettlementRecord", back_populates="loan", cascade="all, delete-orphan")


class FinancialProfile(Base):
    __tablename__ = "financial_profiles"

    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    monthly_income = Column(Numeric(15, 2), nullable=False)
    monthly_expenses = Column(Numeric(15, 2), nullable=False)
    existing_debts = Column(Numeric(15, 2), nullable=False)
    financial_health_score = Column(Integer, nullable=True)

    # Relationships
    borrower = relationship("User", back_populates="financial_profile")


class SettlementRecord(Base):
    __tablename__ = "settlement_records"

    settlement_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    loan_id = Column(Integer, ForeignKey("loans.loan_id", ondelete="CASCADE"), nullable=False)
    settlement_prediction = Column(String(255), nullable=False)
    recommended_amount = Column(Numeric(15, 2), nullable=False)
    priority_level = Column(String(30), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    borrower = relationship("User", back_populates="settlement_records")
    loan = relationship("Loan", back_populates="settlement_records")


class AIHistory(Base):
    __tablename__ = "ai_history"

    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    negotiation_strategy = Column(Text, nullable=False)
    settlement_letter = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    generated_at = Column(DateTime, server_default=func.now())

    # Relationships
    borrower = relationship("User", back_populates="ai_histories")
