from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud, security, database
from .database import engine, get_db
from .config import settings
from .engine.financial import calculate_health_score
from .engine.prediction import evaluate_settlement
from .engine.advisor import generate_negotiation_package

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FinRelief AI API", version="1.0.0")

# Setup CORS to allow React frontend (default http://localhost:5173) to communicate securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Authentication Dependency
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = security.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


# --- API Routes ---

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "FinRelief AI Backend"}


# Auth Router
@app.post("/api/auth/register", response_model=schemas.UserResponse, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/api/auth/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not security.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = security.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Financial Profile Router
@app.get("/api/profile", response_model=schemas.FinancialProfileResponse)
def get_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = crud.get_financial_profile(db, user_id=current_user.user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Financial profile not found. Please create one.")
    return profile


@app.post("/api/profile", response_model=schemas.FinancialProfileResponse)
def save_profile(
    profile: schemas.FinancialProfileCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Calculate health score dynamically
    health_score = calculate_health_score(
        income=profile.monthly_income,
        expenses=profile.monthly_expenses,
        debts=profile.existing_debts
    )
    return crud.create_or_update_financial_profile(
        db=db,
        profile=profile,
        user_id=current_user.user_id,
        health_score=health_score
    )


# Loans Router
@app.get("/api/loans", response_model=List[schemas.LoanResponse])
def get_loans(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_loans_by_user(db, user_id=current_user.user_id)


@app.post("/api/loans", response_model=schemas.LoanResponse, status_code=201)
def add_loan(
    loan: schemas.LoanCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_loan(db=db, loan=loan, user_id=current_user.user_id)


@app.delete("/api/loans/{loan_id}")
def remove_loan(
    loan_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    loan = crud.get_loan(db, loan_id=loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan record not found")
    if loan.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this loan record")
    
    crud.delete_loan(db, loan_id=loan_id)
    return {"message": "Loan record successfully deleted"}


# Settlement Prediction Router
@app.get("/api/settlements", response_model=List[schemas.SettlementRecordResponse])
def get_settlement_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_settlements_by_user(db, user_id=current_user.user_id)


@app.post("/api/settlements/evaluate/{loan_id}", response_model=schemas.SettlementRecordResponse)
def evaluate_loan_settlement(
    loan_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    loan = crud.get_loan(db, loan_id=loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan record not found")
    if loan.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to evaluate this loan")

    profile = crud.get_financial_profile(db, user_id=current_user.user_id)
    if not profile:
        raise HTTPException(
            status_code=400,
            detail="Financial Profile is required prior to generating settlement predictions."
        )

    # Evaluate settlement parameters
    evaluation = evaluate_settlement(
        outstanding_amount=loan.outstanding_amount,
        interest_rate=loan.interest_rate,
        due_date=loan.due_date,
        financial_health_score=profile.financial_health_score or 50
    )

    # Save settlement record to DB
    record = crud.create_settlement_record(
        db=db,
        user_id=current_user.user_id,
        loan_id=loan.loan_id,
        prediction=evaluation["settlement_prediction"],
        recommended=evaluation["recommended_amount"],
        priority=evaluation["priority_level"]
    )
    return record


# AI Negotiation Router
@app.get("/api/negotiations", response_model=List[schemas.AIHistoryResponse])
def get_negotiation_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_ai_histories_by_user(db, user_id=current_user.user_id)


@app.post("/api/negotiate/{loan_id}", response_model=schemas.AIHistoryResponse)
def generate_negotiation(
    loan_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    loan = crud.get_loan(db, loan_id=loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan record not found")
    if loan.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    profile = crud.get_financial_profile(db, user_id=current_user.user_id)
    if not profile:
        raise HTTPException(status_code=400, detail="Financial Profile is required.")

    # Get latest evaluation for this loan
    settlement = db.query(models.SettlementRecord).filter(
        models.SettlementRecord.loan_id == loan_id,
        models.SettlementRecord.user_id == current_user.user_id
    ).order_by(models.SettlementRecord.created_at.desc()).first()

    if not settlement:
        # Evaluate dynamically if no current record exists
        evaluation = evaluate_settlement(
            outstanding_amount=loan.outstanding_amount,
            interest_rate=loan.interest_rate,
            due_date=loan.due_date,
            financial_health_score=profile.financial_health_score or 50
        )
        recommended_amount = evaluation["recommended_amount"]
    else:
        recommended_amount = settlement.recommended_amount

    # Generate strategies and letters
    package = generate_negotiation_package(
        borrower_name=current_user.name,
        email=current_user.email,
        loan_type=loan.loan_type,
        outstanding_amount=loan.outstanding_amount,
        interest_rate=loan.interest_rate,
        recommended_amount=recommended_amount,
        financial_health_score=profile.financial_health_score or 50
    )

    # Save to AI History log
    record = crud.create_ai_history_record(
        db=db,
        user_id=current_user.user_id,
        strategy=package["negotiation_strategy"],
        letter=package["settlement_letter"],
        ai_response=package["ai_response"]
    )
    return record
