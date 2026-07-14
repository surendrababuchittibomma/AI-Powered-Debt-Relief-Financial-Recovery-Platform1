Phase 6: Project Testing
This folder contains the verification protocols, test plans, automated unit test specifications, and performance test summaries for the platform.

1. Test Cases Specification
We built automated Python tests using pytest to verify the mathematical boundaries of the system. These tests are defined in backend/tests/test_financial_engine.py.

Test Case 1: Low Stress Calculation
Target Module: app.services.financial_engine.recalculate_financial_profile
Test Input: User with $10,000 monthly income, $2,000 expenses, and a single $12,000 loan with a $500 monthly payment.
Expected Output:
EMI Ratio = 0.05 (5%)
DTI Ratio = 0.10 (10% of annual income)
Monthly Surplus = $7,500
Stress Level = "Low"
Verification Method: Automated asset comparison assertions.
Test Case 2: Severe Stress Calculation
Target Module: app.services.financial_engine.recalculate_financial_profile
Test Input: User with $3,000 monthly income, $2,500 expenses, and a $15,000 credit card with a $600 monthly payment.
Expected Output:
Monthly Surplus = -$100 (negative surplus)
Stress Level = "Severe"
Verification Method: Automated assertions checking negative surplus boundaries.
Test Case 3: Delinquent Unsecured Settlement Prediction
Target Module: app.services.financial_engine.calculate_settlement_prediction
Test Input: User with $4,000 income ($400 surplus, High stress rating) and a $10,000 credit card balance that is 6 months overdue.
Expected Output:
Target Settlement Percentage = 35% (Base 70% - 25% for 6 months overdue - 5% for High stress - 10% for unsecured credit card. Capped at minimum floor 35%).
Suggested Settlement payoff amount = $3,500
Risk Category = "Severe"
Verification Method: Automated boundary assertion checks.
Test Case 4: Secured Mortgage Active Settlement Prediction
Target Module: app.services.financial_engine.calculate_settlement_prediction
Test Input: User with $5,000 income ($2,000 surplus, Low stress rating) and a active $100,000 secured mortgage that is 0 months overdue.
Expected Output:
Target Settlement Percentage = 85% (Base 70% + 15% markup for secured mortgage. Capped at maximum ceiling 85%).
Suggested Settlement payoff amount = $85,000
Risk Category = "Low"
Verification Method: Checks if secured debt markups function properly.
2. Test Execution Output
We executed our test suite inside the Python environment. Below is the command and successful execution log:

python -m pytest tests
============================= test session starts =============================
platform win32 -- Python 3.13.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\madda\OneDrive\Desktop\My-Projects\smartbridge\backend
plugins: anyio-4.14.1
collected 4 items

tests\test_financial_engine.py ....                                      [100%]

======================== 4 passed, 1 warning in 1.05s =========================
3. Frontend Compilation Build Check
We ran the React bundler compile command to verify compilation soundness:

npm run build
vite v8.1.1 building client environment for production...
transforming...✓ 72 modules transformed.
rendering chunks...
dist/index.html                   0.76 kB │ gzip:  0.46 kB
dist/assets/index-DT8EQEoa.css    6.77 kB │ gzip:  2.15 kB
dist/assets/index-CNSQX8pb.js   295.21 kB │ gzip: 88.00 kB

✓ built in 612ms
Result: The frontend compiled successfully in 612 milliseconds with zero errors or warnings, confirming complete component routing compatibility.
