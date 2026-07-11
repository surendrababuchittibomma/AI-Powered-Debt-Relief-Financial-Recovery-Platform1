Phase 4: Project Planning Phase
This folder details the development timeline, sprint schedules, and milestone targets for the platform.

1. Project Milestones
Milestone	Target Deliverable	Completion Status
Milestone 1	Backend Foundation: SQLite connection, SQLAlchemy tables, and Pydantic schemas.	Completed
Milestone 2	Auth & Security: Direct bcrypt password hashing and JWT token exchange.	Completed
Milestone 3	Core Business Logic: Ratios and rule-based settlement prediction calculators.	Completed
Milestone 4	AI Service: Google Gemini integration and local fallback mockup engine.	Completed
Milestone 5	Frontend UI: React Vite initialization and Vanilla CSS styling system.	Completed
Milestone 6	Frontend Components: Dashboard dials, predictor logs, and letter generators.	Completed
Milestone 7	Testing & Launch: Python pytest unit testing and production deployment.	Completed
2. Work Breakdown Structure (WBS)
Sprint 1: Backend Initialization & Database Modeling
Set up FastAPI folder structure, define python dependency packages, and initialize virtual environment (venv).
Establish configuration scripts (config.py) to read environment variables and API keys.
Define SQLAlchemy database models (models.py) reflecting the 6 target relational tables.
Establish session makers and database engines inside database.py.
Sprint 2: Core Calculations & Security Layer
Write mathematical algorithms inside financial_engine.py to evaluate monthly surpluses, DTI ratios, and EMI parameters.
Integrate direct bcrypt password verification and generate token structures inside auth.py.
Implement JWT-header parsing dependencies to authenticate API endpoints.
Sprint 3: Generative AI & API Routing
Integrate the Google Gemini SDK inside gemini_service.py to compile letters and strategies in JSON format.
Write the rule-based local backup text generator to handle offline runs without crashing.
Declare CRUD API routers inside main.py covering user profiles, loan items, predictions, and negotiation history logs.
Sprint 4: Frontend Development & Dials
Scaffold the React project using Vite and write global Token CSS scripts inside index.css.
Build the AuthContext to handle register actions and persist login keys.
Develop user pages: Login, Register, and Dashboard.
Write custom SVG elements on the dashboard to render the animated debt stress level gauge.
Sprint 5: Predictor, Generator & History Logs
Develop the SettlementPredictor page to show target savings and payment timeline structures.
Develop the LetterGenerator page with dropdowns for hardships and buttons to copy or download output files.
Develop the History page utilizing expanding accordion containers for historical audits.
Sprint 6: Testing, Restructuring & Deployments
Write unit tests in pytest to verify math boundaries (Low vs Severe stress indices).
Compile React assets using npm run build to verify syntax and path configurations.
Deploy backend to Railway, configure environment variables, and create public DNS endpoints.
