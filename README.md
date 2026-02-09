# Tester


# logs_out 
 {
  'log_type':
    ['intent_classifier', 'extraction_model' , main_model, ...........],
      'intent_classifier': 'general_chat',
     
      'extraction_answers': 
                ['uncertain', 'medium', 'medium', 'not_sure', 'medium', 'medium']
}



T1:
{
  "normal_path": false,
  "Log_error": {
    "name": "Unexpected intent classification",   #############################
    "details": "intent_classifier: general_chat"  #############################

  },
  "actual": {
    "present_log_types": [
      "main_model",
      "intent_classifier",
      "extraction_model"
    ]
  },
  "Lost_expected_log": {
    "log_type": "memory_extraction",     ############################  
    
    "reason": "User revealed preference for stability property"
  }
}

# Problem 0
     عايز اسو ال error الحقيقي لو ظهر 
Add to prompt : Memoery rules , intent_classifier types




# problem 1

Log Analyzer – Input: 
- Last real agent message:  response 1  : Stability is a strong reason to buy,
- User response: : hello i need to buy a new property for stability

add role , content 0 :
 hello iam real estate agent how can i help you


انا مش عايز رده - انا عايز سؤال و اجابة و لوج 

first user message : real + user

- rael 1 : how can i help
- user 1 : i need condo 
- logs

- real : Stability is a strong reason , when to move ?
- user : 6 months
- logs

OR
==========================================
problem 1:    user_message : n-1 delay with logs   
logs b with user mess A


problem 2 : repeat json 

problem 3 : extraction memory always needed ?  or p1

json needs parse 


TESTER/
├── app/
│   ├── main.py                     # Entry point (python -m app.main)
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py             # env + constants
│   │   └── types.py
        └── logger.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── llm/
│   │   │   └── driver.py            # llm_driver
│   │   ├── logs/
│   │   │   ├── reader.py            # LogsReader
│   │   │   ├── analyser.py          # log_analyser
│   │   │   └── checker.py           # build_Logs_checker_prompt
│   │   ├── orchestration/
│   │   │   └── orchestrator.py
│   │   ├── persona/
│   │   │   ├── persona.py
│   │   │   └── prompts.py
│   │   └── utils/
│   │       └── json_utils.py
│   ├── clients/
│   │   ├── chat_client.py
│   │   └── logs_client.py
│   ├── routes/
│   │   ├── run.py                  # /run tester
│   │   
│   ├── dto/
│   │   └── schemas.py              # pydantic models (reports, logs, etc.)
│   └── __init__.py
├── .env.example   : OPENAI_API_KEY
├── .gitignore
├── README.md
├── requirements.txt






++ out :  

{
'log_type': ['main_model', 'intent_classifier', 'extraction_model'], 

'intent_classifier': 'property_search',
'extraction_answers': ['no', 'family_growth', 'unknown', 'researching']
}       



Logs_analyser : 
``` { "normal_path": true,
 "Log_error": null,
  "actual": [ "main_model","intent_classifier", "extraction_model" ],
    "Lost_expected_log": null,
    
    "intent_response": "property_search",
    "extraction_answers": [ "uncertain", "balanced" ],
    "bug_description": null } ```


