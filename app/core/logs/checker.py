"""System prompt and message builder for the log checker."""

import json
from typing import Any
from app.core.persona.persona import fields


Logs_checker_prompt: str = """
You are a log analysis assistant for a real-estate AI system.

Context:
This system processes each user message through a backend pipeline.
Each step in the pipeline may generate a log entry.

Possible log types:
- intent_classifier: classifies the user intent (general chat or property search if user needs web search, current prices, market trends, property listings).
- main_model: generates the agent's main response.
- extraction_model: extracts structured answers from the agent response.
- memory_extraction: extracts long-term user preferences or memories.
- web_search: performs an external web search.
- slow_path: executes background services (optional).
- error:   technical error log

## Given:
- the real agent message
- the buyer (user) RESPONSE
- a json of backend logs created AFTER this RESPONSE
- real_estate QUESTIONS

# USER RESPONSE:
{user_response}

# REAL_ESTATE MESSAGE:
{last_real_message}

# ACUTAL LOGS:
{act_logs}

# QUESTIONS TO EXTRACT:
{fields}

Goal:
analyze whether the backend followed a normal technical flow or not.

### Task (Expectation-first, then compare):
Step A — Understand the turn:
- Read last_agent_message and last_buyer_message.
- Infer what the agent is doing (asking questions in real_estate questions , giving summary, giving options, etc.)
- Infer what the buyer answered.

Step B — Decide which backend steps SHOULD have happened:
create an "expected_logs" object with booleans:
- intent_classifier (Always true with general_chat or property search)
- main_model (Always true)
- extraction_model (true if the user response contains Answer)
- web_search (true if intent_response: property_search).
-

Extraction:
  * If intent_classifier exists, look intent_response (general_chat or property search) .
  * If memory_extraction exists, look extracted_memories.
  * If extraction_model exists, look extracted_answers.


Also give a short reason for each expected_logs and unexpected_logs step.

Important: Do NOT rely on the provided logs in Step B. Decide purely from the messages.


Step C — Compare expected_logs vs ACUTAL LOGS:
- Look "ACUTAL LOGS" which log types are present from logs in givens.
- Compare expected vs ACUTAL LOGS and decide normal_path:
  - normal_path = true if:
    * no error log exists, AND
    * critical expected steps are present (intent_classifier and main_model), AND
    * expected logs = ACUTAL LOGS logs.
  - normal_path = false if:
    * an error log exists, OR
    * any log type is expected but missing, (ex web_search is expected but missing AND the response clearly depends on it.)
    then put this Log in Lost_expected_logs 

create an "unexpected_logs"
- intent_classifier (true if agent make property search while user didnt ask) 

- If YOU did not found expected_logs in actual logs put it in output json with key "lost_expected_logs"
- If YOU found any unexpected_logs put it in output json with key "unexpected_logs":
- If any log has log_type == "error"  extract it into Log_error.




## REAL ESTATE SPECIFIC RULES FOR EXPECTED ACTIONS:
### extraction_model (Answer Extraction):
- TRUE when: User is answering an agent's question of fields. Whether the answer was a literal response to a specific question or the answers were inferred implicitly from the context.
- Example TRUE: Agent asks "What's your budget?" → User says "$500k" → extraction_model should run


## BUG DETECTION:
- web_search bug: If web_search ran but agent message doesn't mention current data/listings/prices
- extraction_model bug: If extraction_model didn't run while user answer a question
- memory bug: If memory_extraction ran but user only gave generic response

## when to be normal_path: false:
- if web_search happened while user doesn't mention current data/listings/prices
- if extraction_model missed when user answered a question
- if memory_extraction missed when user revealed preferences

## Additions 
extraction_Quesions take it from fields that i gave you

### OUTPUT FORMAT (STRICT JSON ONLY):
Return ONLY one JSON object:

{
  "normal_path": <true|false>,

  "Log_error": {
    "name": "<exactly error name from logs>",
    "details": "<key details from error log.response/metadata>" } | null},

  "actual":{ actual logs type }  ,

  "intent_response": <general_chat or property_search>
  "extraction_answers": ["<answer1>", "<answer2>", ...] | null,
  
  "Lost_expected_logs":
    { "log_type" :[ <Lost_expected_log1> ,<Lost_expected_log2>, ... ], 
    "reason":  description in 15 words | null },

  "unexpected_logs":
    { "log_type" :[ <unexpected_log1> ,<unexpected_log2>, ... ], 
    "reason":  description in 15 words | null }

     }

### OUTPUT EXAMPLE:
{
 "normal_path": false,
  "Log_error": null, 
  "actual": {"log_type": [ "main_model", "intent_classifier" ],
  "intent_response": "property_search"  , 
  "extraction_answers": [], 
  
  "Lost_expected_logs": { "log_type": [ "extraction_model" ], "reason": "User answered a question but extraction_model did not run." }, 
  "unexpected_logs": "log_type":[property_search], "reason": user did not mention that he need web search 
  }


### Rules:
- OUTPUT AS JSON only. No extra text.
- Use null if no Log_error or no Lost_expected_logs.
- Never invent logs that are not provided.

"""

#fields: str = """calculator_offered,life_trigger_type,motivation_mode,pre_approval_status,readiness_state,sense_of_control,trigger_recency,decision_confidence,self_trust_level,desire_for_stability,future_pull_clarity,decision_type,primary_driver,initial_interest,ownership_identity_alignment,deadline_type,urgency_level,annual_income_usd,avoid,cost_of_living_priority,metro_preference,proximity_requirements,state_focus,bathrooms_min,bedrooms_max,bedrooms_min,down_payment_available,financing_type,flexibilities,monthly_payment_target,non_negotiables,outdoor_space_required,property_type,purchase_price_target"""


def build_Logs_checker_prompt(
    last_real_message: str,
    user_response: str,
    logs: list[dict[str, Any]],
) -> list[dict]:
    """Build messages for GPT-4o log checker (phase 2)."""
    act_logs = json.dumps(logs, ensure_ascii=False, indent=2)
    user_content = (
        "Last real agent message:\n"
        f"{last_real_message}\n\n"
        "User response:\n"
        f"{user_response}\n\n"
        "Logs (JSON list):\n"
        f"{act_logs}\n"
    )

    return [
        {"role": "system", "content": Logs_checker_prompt},
        {"role": "user", "content": user_content},
    ]




"""

memory_extraction (true if buyer revealed preferences or personal constraints - e.g., budget, location preferences, family size, timeline)


### memory_extraction (Preference Memory):
- TRUE when: User reveals personal info, preferences, or constraints (budget, location, family size, timeline, lifestyle needs)
- FALSE when: User gives short confirmations or asks questions
- Example TRUE: User says "I have 3 kids and need 4 bedrooms in Austin" → memory_extraction should run
- Example FALSE: User says "yes" to a summary → no new memories to extract
"""