Phase 7: Project Documentation
This folder contains the complete operational instructions, user manuals, and run guides for BlogForge - AI Powered Debt Relief & Financial Recovery Platform.

1. System Requirements
Operating System: Windows, macOS, or Linux.
Python Environment: Python 3.11 or newer (tested on Python 3.13.6).
Node Environment: Node.js v18 or newer (tested on Node.js v22.18).
Package Manager: npm v9 or newer.
2. Installation & Local Setup
Step 1: Clone the Repository
Open your terminal and clone your GitHub repository:

git clone https://github.com/suryaprabhat/BlogeForge_AI-Debt-Relief.git
cd BlogeForge_AI-Debt-Relief
Step 2: Configure the Backend Environment
Navigate to the backend directory:
cd "5. Project Development Phase/backend"
Create a virtual environment:
python -m venv venv
Activate the virtual environment:
Windows (PowerShell): .\venv\Scripts\Activate.ps1
macOS / Linux: source venv/bin/activate
Install the required packages:
pip install -r requirements.txt
Configure your environment variables. Create a .env file inside the backend/ directory:
# Google Gemini API key from AI Studio
GEMINI_API_KEY=your_actual_gemini_api_key_here
Step 3: Configure the Frontend Environment
Navigate to the frontend directory:
cd "../frontend"
Install the required Node packages:
npm install
Create a .env file inside the frontend/ directory (for pointing to the local backend during development):
VITE_API_URL=http://127.0.0.1:8000
3. Running the Applications Locally
To run the application locally, you must start both the backend API server and the frontend client dev server:

1. Launch the Backend API (Terminal 1)
Make sure you are in the /backend folder and your virtual environment is active, then run:

python run.py
The FastAPI server will boot and listen on http://127.0.0.1:8000. You can access the interactive Swagger API documentation at http://127.0.0.1:8000/docs.

2. Launch the Frontend Dev Server (Terminal 2)
Make sure you are in the /frontend folder, then run:

npm run dev
Vite will spin up the web client at http://localhost:5173/. Open this URL in your web browser.

4. User Guide & Core Features
1. Account Setup
Click Create Account and register with your email and name.
Upon logging in, click Profile Settings and configure your Monthly Income and Basic Expenses. This is crucial for calculating your debt ratios accurately.
2. Loan Management
Click Add Loan Account on the dashboard.
Enter details of your outstanding balances, active interest rates (APR), monthly EMI obligations, and overdue duration (months delinquent).
The dashboard will automatically update your overall Total Debt, Total monthly EMIs, and Monthly Surplus, and plot your Debt Distress Level (Low, Medium, High, or Severe) on the custom visual dial.
3. Settlement Prediction
Go to the Settlement Predictor page.
Select an active loan. The engine will calculate target payoff values (e.g. 35% to 55% of the total balance) and evaluate your default risk level.
It will display structured payoff plans, detailing single lump-sum payoffs vs. structured 3-month/6-month installment schedules.
4. Drafting AI Hardship Letters
Go to the AI Letter Generator page.
Select the creditor account, select a primary hardship reason (Job Loss, Medical Issue, etc.), and provide brief supporting details.
Click Generate. The Google Gemini API will construct a custom formal proposal.
Copy the compiled letter text or click Download to save it as a text file to print or mail to the creditor.
Access past letters at any time on the History & Logs tab.
