"""FastAPI route for running the tester."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.config.types import RunReport, Turn

from app.config.settings import (
    API_URL,
    USER_ID,
    OPENAI_MODEL,
    TIMEOUT_SEC,
    RETRY_COUNT,
    MAX_TURNS,
    MAX_TOTAL_SECONDS,
    INITIAL_USER_MESSAGE,
    INITIAL_REAL_Estate_MESSAGE
)
from app.clients.chat_client import ChatClient
from app.core.llm.driver import LLMDriver
from app.core.orchestration.orchestrator import Orchestrator 
from app.config.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()



@router.post("/run", response_model=RunReport, response_model_exclude_none=True)
async def run_tester():
    """Run the AI tester and return the report."""
    try:
        logger.info("Starting tester run")
        chat = ChatClient(API_URL, USER_ID, TIMEOUT_SEC, RETRY_COUNT)
        driver = LLMDriver(OPENAI_MODEL, api_key_env="OPENAI_API_KEY")
        orchestrator = Orchestrator(chat, driver, MAX_TURNS, MAX_TOTAL_SECONDS)
        report = orchestrator.run(INITIAL_USER_MESSAGE, INITIAL_REAL_Estate_MESSAGE)
        session_id = report.session_id
        
        if report.final_summary:
            logger.info("Final summary generated")
        else:
            logger.info("Run completed without final summary")

        return RunReport(
            success=report.success,
            user_id=  USER_ID,
            session_id=session_id ,
            turns=[Turn(role=t.role, user_id=  USER_ID, session_id= t.session_id    , content=t.content, ts=t.ts, logs_report=t.logs_report) for t in report.turns],
            final_summary=report.final_summary,
            started_at=report.started_at,
            ended_at=report.ended_at,
            error=report.error
        )
    except Exception as e:
        logger.error(f"Error running tester: {e}")
        raise HTTPException(status_code=500, detail=str(e))
