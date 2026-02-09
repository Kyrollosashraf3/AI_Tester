"""FastAPI route for running the tester."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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


class TurnModel(BaseModel):
    role: str
    content: str
    ts: datetime
    logs_report: Optional[str] = None


class RunReportModel(BaseModel):
    success: bool
    turns: List[TurnModel]
    final_summary: Optional[str]
    started_at: datetime
    ended_at: datetime
    error: Optional[str]


@router.post("/run", response_model=RunReportModel)
async def run_tester():
    """Run the AI tester and return the report."""
    try:
        logger.info("Starting tester run")
        chat = ChatClient(API_URL, USER_ID, TIMEOUT_SEC, RETRY_COUNT)
        driver = LLMDriver(OPENAI_MODEL, api_key_env="OPENAI_API_KEY")
        orchestrator = Orchestrator(chat, driver, MAX_TURNS, MAX_TOTAL_SECONDS)
        report = orchestrator.run(INITIAL_USER_MESSAGE, INITIAL_REAL_Estate_MESSAGE)

        if report.final_summary:
            logger.info("Final summary generated")
        else:
            logger.info("Run completed without final summary")

        return RunReportModel(
            success=report.success,
            turns=[TurnModel(role=t.role, content=t.content, ts=t.ts, logs_report=t.logs_report) for t in report.turns],
            final_summary=report.final_summary,
            started_at=report.started_at,
            ended_at=report.ended_at,
            error=report.error
        )
    except Exception as e:
        logger.error(f"Error running tester: {e}")
        raise HTTPException(status_code=500, detail=str(e))
