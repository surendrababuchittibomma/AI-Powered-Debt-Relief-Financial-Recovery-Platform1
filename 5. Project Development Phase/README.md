Phase 5: Project Development Phase
This folder contains the complete, production-ready codebase for BlogForge - AI Powered Debt Relief & Financial Recovery Platform, organized into backend and frontend components.

1. Codebase Structure
The source code is organized into two primary subdirectories:

📁 Backend (backend/)
Built with Python FastAPI, SQLite (local), and SQLAlchemy ORM.

app/main.py: API routes for JWT authentication, user profiles, loan management, and AI letter generation.
app/models.py: Relational SQLAlchemy database models mapping to the SQLite/Postgres tables.
app/schemas.py: Pydantic validation schemas.
app/auth.py: User authentication utility functions utilizing direct bcrypt password hashing and JWT encoding/decoding.
app/services/financial_engine.py: Business logic calculators for DTI ratios, EMI ratios, surplus cash flow, and rule-based predictions.
app/services/gemini_service.py: Google Gemini API client integration for hardship letter compilation, complete with a high-fidelity local mockup generator fallback.
tests/: Pytest automated unit tests verifying calculator boundaries.
requirements.txt: Python dependencies list.
run.py: FastAPI server startup execution script.
📁 Frontend (frontend/)
Built with React.js (Vite) and Vanilla CSS.

src/index.css: Design Token styling utilizing responsive grids, HSL variable systems, custom neon glows, glassmorphic cards, and keyframe animations.
src/context/AuthContext.jsx: Manages session state, local tokens, user registrations, and dynamic API URL lookups.
src/pages/Login.jsx & Register.jsx: User credentials management views.
src/pages/Dashboard.jsx: Commands summary cards, loan tables, CRUD modals, and the custom SVG visual gauge of the borrower's distress score.
src/pages/SettlementPredictor.jsx: Displays target settlement amounts, warning badges, comparison bars, and structured lump-sum vs. installment payment plans.
src/pages/LetterGenerator.jsx: UI for AI letter generation inputs, displaying suggested bulleted strategies, and buttons to copy or download files.
src/pages/History.jsx: Accordion logs of past generated letters.
vercel.json: SPA routing rewrite rules for Vercel edge deployment.
2. Core Functional Features Implemented
JWT Authentication: Secure login and registration with hashed password persistence.
Interactive Dashboard: Real-time evaluation of total debt liabilities, gross income, and basic living expenses.
Visual Stress Meter: Custom animated dial reflecting the borrower's debt distress score based on calculated DTI and EMI ratios.
Adaptive Settlement Predictor: Suggests realistic target settlement percentages (ranging from 35% to 85%) based on delinquency duration, loan type (secured vs. unsecured), and financial stress.
Structured Payoff Plans: Automatically breaks down predicted settlement values into immediate single lump-sum payoffs vs. structured 3-month or 6-month payment schedules.
AI Negotiation Letter Generator: Triggers Google Gemini API to draft professional, personalized hardship letters using input parameters and custom text inputs.
Auto Fallback Engine: If the Gemini API key is missing or offline, the local mock generator automatically runs, compiling letters without throwing server crashes.
Audit Logs & History: Expandable accordion log list showing all past proposal documents.
