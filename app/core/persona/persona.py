"""Persona definition and question/stop detection."""

import re

PERSONA: dict = {
    "motivation": "i am Sam - i need to buy for stability, family with kids",
    "target_buy_date": "Feb 2027 (flexible)",
    "comfort_with_process": "7/10",
    "main_stress": "getting approved",
    "annual_income_usd": 120000,
    "down_payment_available": 200000,
    "state_focus": "New Jersey",
    "area_focus": "Wayne (ok nearby: Pequannock/Riverdale if needed)",
    "purchase_budget_max": 200000,
    "property_type": "condo",
    "bedrooms_min": 3,
    "bathrooms_min": 2,
    "monthly_payment_target": 3000,
    "condition_preference": "light cosmetic updates ok",
    "proximity_requirements": "Wayne Hills High School and Pompton Lakes",
    "max_drive_time": "30 minutes",
    "quiet_environment_preference": "quiet",
    "safety_importance": "10/10",
    "outdoor_space_required": "optional; small patio nice-to-have",
    "deadline_type": "flexible",
}

QUESTION_STARTERS = (
    "how ",
    "what ",
    "which ",
    "when ",
    "where ",
    "why ",
    "do you ",
    "are you ",
    "on a scale ",
)


def persona_context() -> dict:
    """Return a copy of the persona dict for context."""
    return dict(PERSONA)



fields: str = """
Has the pre-approval calculator been offered?
What's happening in your life now?
Why are you buying a home?
Have you been pre-approved by a lender?
How ready are you for the next step?
How comfortable are you with the process?
When do you want to buy?
How confident are you in making decisions?
How much do you trust your own judgment?
How important is stability to you?
How clear is your vision of the future?
How do you usually make decisions?
What matters most to you in this purchase?
What sparked your interest in buying?
How well does homeownership fit your identity?
Do you have a specific deadline?
How urgent does this feel to you?
What is your annual income?
What are your deal-breakers for location?
How important is affordability?
Do you prefer urban, suburban, or rural?
What do you need nearby?
Which state are you looking in?
Minimum number of bathrooms?
Maximum number of bedrooms?
Minimum number of bedrooms?
How much can you put down?
How do you plan to finance?
What are your nice-to-haves?
What monthly payment are you comfortable with?
What are your must-haves?
Do you need outdoor space?
What type of home do you want?
What's the average home price you're considering?
"""
