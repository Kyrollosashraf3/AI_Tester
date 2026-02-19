# AI Tester

## Project Overview

AI Tester is a FastAPI-based application designed to test AI chat systems (Real Estate Agent), analyze logs, and generate detailed reports on conversation quality.

---

## Features

- **Automated AI Chat Testing**: Run automated conversations between a buyer and the real estate agent
- **Log Analysis**: Analyze backend logs to detect errors and abnormal paths
- **Conversation Orchestration**: Manage conversation turn-by-turn until summary or limits are reached
- **Web Interface**: Easy-to-use web interface for running tests
- **OpenAI Integration**: Uses GPT-4o for generating buyer persona replies
- **Duplicate Question Detection**: Detect repeated questions using semantic similarity

---

## Project Structure

```
AI_Tester/
├── main.py                           # Application entry point
├── requirements.txt                  # Project dependencies
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore file
├── templates/
│   └── index.html                   # Main web page
└── app/
    ├── __init__.py
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py              # Settings and constants
    │   ├── types.py                # Type definitions (DataClasses)
    │   └── logger.py               # Logging configuration
    ├── clients/
    │   ├── __init__.py
    │   ├── chat_client.py          # Chat client (SSE)
    │   ├── logs_client.py          # Logs API client
    │   └── embeddings.py           # Embeddings generation
    ├── core/
    │   ├── __init__.py
    │   ├── llm/
    │   │   ├── __init__.py
    │   │   └── driver.py            # LLM driver (GPT-4o)
    │   ├── logs/
    │   │   ├── __init__.py
    │   │   ├── reader.py           # Logs reader
    │   │   ├── analyser.py         # Logs analyser
    │   │   └── checker.py          # Logs checker
    │   ├── orchestration/
    │   │   ├── __init__.py
    │   │   ├── chat.py             # Chat orchestrator
    │   │   └── report.py           # Report orchestrator
    │   └── persona/
    │       ├── __init__.py
    │       ├── persona.py           # Buyer persona definition
    │       ├── tracker.py           # Question tracker & stop conditions
    │       └── prompts.py           # System prompts
    └── routes/
        ├── __init__.py
        ├── run_chat.py              # /chat route
        └── run_report.py            # /report route
```

---

## Main Components

### 1. Application Settings (`app/config/settings.py`)

- `API_URL`: Real Estate Agent API endpoint
- `LOGS_API_URL`: Logs API endpoint
- `OPENAI_MODEL`: OpenAI model to use (gpt-4o)
- `TIMEOUT_SEC`: Request timeout in seconds
- `RETRY_COUNT`: Number of retry attempts
- `MAX_TURNS`: Maximum number of conversation turns
- `MAX_TOTAL_SECONDS`: Maximum total time limit
- `INITIAL_USER_MESSAGE`: Initial user message
- `INITIAL_REAL_Estate_MESSAGE`: Initial real estate agent message

### 2. Buyer Persona (`app/core/persona/persona.py`)

The `PERSONA` dictionary defines the buyer persona:

```python
PERSONA = {
    "motivation": "i am Sam - i need to buy for stability, family with kids",
    "target_buy_date": "Feb 2027 (flexible)",
    "annual_income_usd": 120000,
    "down_payment_available": 200000,
    "state_focus": "New Jersey",
    "area_focus": "Wayne",
    "purchase_budget_max": 200000,
    "property_type": "condo",
    "bedrooms_min": 3,
    "bathrooms_min": 2,
    # ... and more
}
```

### 3. API Clients

- **ChatClient** (`app/clients/chat_client.py`): Client for connecting to Real Estate Agent via Server-Sent Events (SSE)
- **LogsApiClient** (`app/clients/logs_client.py`): Client for fetching logs from the backend
- **LLMDriver** (`app/core/llm/driver.py`): Driver for generating buyer replies using GPT-4o

### 4. Log Analyzers

- **LogsReader** (`app/core/logs/reader.py`): Read and process new logs
- **LogAnalyser** (`app/core/logs/analyser.py`): Analyze logs using GPT-4o
- **LogsChecker** (`app/core/logs/checker.py`): Validate logs and detect errors

### 5. Routes (API Endpoints)

- **`POST /chat`**: Run simple chat test
- **`POST /report`**: Run detailed report test with log analysis

---

## Possible Log Types

- `intent_classifier`: Classifies user intent
- `main_model`: Generates main agent response
- `extraction_model`: Extracts answers from user responses
- `memory_extraction`: Extracts user preferences and memories
- `web_search`: Performs external web search
- `slow_path`: Executes background services
- `error`: Technical error log

---

## Output Examples

### Example of Logs Output:

```json
{
  "log_type": [
    "main_model",
    "intent_classifier",
    "extraction_model"
  ],
  "intent_classifier": "general_chat",
  "extraction_answers": [
    {
      "qid": "initial_interest",
      "answer": "stability"
    },
    {
      "qid": "motivation_mode",
      "answer": "lifestyle"
    }
  ]
}
```

### Example of Analysis Report:

```
json
{
  "normal_path": true,
  "Log_error": null,
  "actual": {
    "log_type": [
      "main_model",
      "intent_classifier",
      "extraction_model"
    ]
  },
  "intent_response": "property_search",
  "extraction_answers": ["uncertain", "balanced"],
  "Lost_expected_log": null,
  "unexpected_logs": null,
  "bug_description": null
}
```

---

## Installation

1. Clone the repository:
```
bash
git clone <repository-url>
cd AI_Tester
```

2. Install dependencies:
```
bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file and add:
```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Running the Application

1. Start the application:
```
bash
uvicorn main:app --reload
```

2. Open your browser at `http://localhost:8000` for the web interface

3. Or use the API directly:
```
bash
# Run chat test
curl -X POST http://localhost:8000/chat

# Run report test
curl -X POST http://localhost:8000/report
```

---

## Usage

### Via Web Interface:

1. Open the main page `http://localhost:8000`
2. Click "Run Chat" for simple testing
3. Or click "Run Report" for detailed testing with log analysis
4. View the results on the page

### Via API:

```
python
import requests

response = requests.post("http://localhost:8000/chat")
print(response.json())
```

---

## Advanced Configuration

You can modify settings in `app/config/settings.py`:

- `API_URL`: Real Estate Agent API endpoint
- `LOGS_API_URL`: Logs API endpoint
- `OPENAI_MODEL`: OpenAI model (default: gpt-4o)
- `TIMEOUT_SEC`: Request timeout (default: 50 seconds)
- `RETRY_COUNT`: Number of retries (default: 2)
- `MAX_TURNS`: Maximum turns (default: 2)
- `MAX_TOTAL_SECONDS`: Maximum total time (default: 2000 seconds)

---

## Troubleshooting

### 1. OpenAI Authentication Error
- Make sure `OPENAI_API_KEY` is correct in `.env` file

### 2. Real Estate Agent API Connection Error
- Make sure `API_URL` is correct and reachable

### 3. Logs Fetching Error
- Make sure `LOGS_API_URL` is correct

---

## Duplicate Question Detection

The system uses Cosine Similarity to detect duplicate questions:

1. Generate embeddings for all questions
2. Calculate similarity matrix
3. Group similar questions together
4. Return only duplicated questions

---

## Notes

- The project uses FastAPI as the web framework
- Uses uvicorn as the ASGI server
- Relies on requests for external API communication
- Uses python-dotenv for environment variable management

---

## Workflow Example

1. **Conversation Start**:
   - Agent asks: "What's happening in your life right now?"
   - Buyer replies: "I need to buy a property for stability"

2. **Logs Reading**:
   - Read logs from the server
   - Analyze if paths are correct

3. **Reply Generation**:
   - LLM driver generates buyer reply based on persona
   - Uses previous questions and context

4. **Repetition**:
   - Continue until agent provides summary or limits are reached

5. **Reporting**:
   - Return comprehensive report including:
     - All turns
     - Log analysis
     - Duplicate questions (if any)
     - Conversation summary

---

## License

MIT License

---

## Developer

Developed by AI Testing Team
