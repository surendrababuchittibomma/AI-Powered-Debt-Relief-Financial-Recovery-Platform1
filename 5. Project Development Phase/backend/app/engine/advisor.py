import requests
import json
from decimal import Decimal
from ..config import settings

def generate_negotiation_package(
    borrower_name: str,
    email: str,
    loan_type: str,
    outstanding_amount: Decimal,
    interest_rate: Decimal,
    recommended_amount: Decimal,
    financial_health_score: int
) -> dict:
    """
    Generates a negotiation strategy and custom settlement letter.
    Tries to call Google Gemini API if configured, otherwise falls back to dynamic templates.
    """
    # 1. Fallback Template Builder
    strategy_template = f"""### Step-by-Step Negotiation Strategy for {borrower_name}

1. **Initiate Contact (Hardship Declaration)**:
   - Call the creditor and declare a formal financial hardship. Explain that your current Financial Capacity Score is low ({financial_health_score}/100) and that you are seeking a mutually beneficial payoff solution to avoid defaulting.

2. **Propose the Lump-Sum Payoff**:
   - Offer the recommended settlement amount of **${recommended_amount:,.2f}** (which represents a discounted portion of your total outstanding balance of ${outstanding_amount:,.2f}).
   - Clarify that these funds are sourced from family assistance or asset liquidation, implying this is a one-time offer.

3. **Negotiate Credit Reporting Terms (Pay-for-Delete)**:
   - Request that the creditor reports the account as "Paid in Full" or deletes the negative trade line entirely upon clearing of the settlement funds.

4. **Verify Settlement in Writing**:
   - Do **NOT** send any payments until you receive a formal, written settlement agreement from the lender specifying the exact payoff sum and reporting terms.
"""

    letter_template = f"""[Date]

To: Settlement & Recovery Department
Regarding: Account Settlement Proposal
Account Holder: {borrower_name}
Associated Email: {email}
Debt Instrument: {loan_type}
Current Outstanding Balance: ${outstanding_amount:,.2f}
Proposed Payoff Settlement Amount: ${recommended_amount:,.2f}

Dear Sir/Madam,

I am writing this letter to formally request a settlement of the outstanding debt mentioned above. Due to unexpected financial difficulties, my monthly obligations exceed my disposable income, rendering it impossible to pay the full outstanding balance.

After reviewing my budget, I am able to offer a one-time, lump-sum payment of **${recommended_amount:,.2f}** as a full and final settlement of this account. This amount is the maximum I can secure at this time.

If you agree to accept this amount as payment in full, please send me a written confirmation letter stating that:
1. The proposed settlement sum of ${recommended_amount:,.2f} will release me from all liabilities for this account.
2. The account status will be reported to credit bureaus as "Paid in Full" or "Settled in Full".

Upon receipt of your written agreement, I will immediately process the payment.

Sincerely,

{borrower_name}
Email: {email}
"""

    # If key is available, try to fetch from Gemini API
    if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "mock_key":
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            prompt = (
                f"You are a professional debt negotiation and financial recovery advisor. "
                f"Create a custom negotiation strategy and a formal settlement letter for a debtor named {borrower_name} (email: {email}) "
                f"who has an outstanding {loan_type} balance of ${outstanding_amount} at {interest_rate}% interest rate. "
                f"We recommend settling for ${recommended_amount}. Their financial health score is {financial_health_score}/100. "
                f"Return the response strictly as a JSON object containing the keys: "
                f"'negotiation_strategy' (markdown text) and 'settlement_letter' (formatted text letter)."
            )
            
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=8)
            if response.status_code == 200:
                data = response.json()
                content_text = data['candidates'][0]['content']['parts'][0]['text']
                parsed_content = json.loads(content_text)
                return {
                    "negotiation_strategy": parsed_content.get("negotiation_strategy", strategy_template),
                    "settlement_letter": parsed_content.get("settlement_letter", letter_template),
                    "ai_response": "Gemini API Generated"
                }
        except Exception as e:
            # Silence and proceed to fallback
            pass

    return {
        "negotiation_strategy": strategy_template,
        "settlement_letter": letter_template,
        "ai_response": "Template Engine Fallback (Offline Mode)"
    }
