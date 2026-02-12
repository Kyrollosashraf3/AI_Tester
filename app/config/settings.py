"""Configuration constants for Phase 1 tester."""

# production
#API_URL: str = "........."
#LOGS_API_URL: str = "........."

# stage
API_URL: str = "........."
LOGS_API_URL: str = "........."



from uuid import uuid4
USER_ID = str(uuid4())

OPENAI_MODEL: str = "gpt-4o"
TIMEOUT_SEC: int = 50
RETRY_COUNT: int = 2
MAX_TURNS: int = 40
MAX_TOTAL_SECONDS: int = 2000
INITIAL_USER_MESSAGE: str = "hello i need to buy a new property for stability"
INITIAL_REAL_Estate_MESSAGE: str = "what’s happening in your life right now that’s making you consider buying"


LOGS_LIMIT: int = 50
