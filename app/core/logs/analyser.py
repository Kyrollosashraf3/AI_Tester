"""Log analyser for phase 2."""

import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

from app.core.logs.checker import build_Logs_checker_prompt
from app.config.logger import get_logger

logger = get_logger(__name__)


class LogAnalyser:
    """Uses OpenAI GPT-4o to analyze logs."""

    def __init__(self, model: str = "gpt-4o", api_key_env: str = "OPENAI_API_KEY"):
        self.model = model
        api_key = os.environ.get(api_key_env)
        if not api_key:
            logger.error(f"Missing {api_key_env} environment variable")
            raise ValueError(f"Missing {api_key_env} environment variable")
        self._client = OpenAI(api_key=api_key)
        logger.info("LogAnalyser initialized")

    def analyse(
        self,
        last_assistant: str,
        user_response: str,
        logs: list[dict[str, Any]],
    ) -> str:
        """Analyze logs for normal path."""
        messages = build_Logs_checker_prompt(last_assistant, user_response, logs)
        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=200,
                temperature=0.0,
            )
            content = resp.choices[0].message.content
            logger.info("Log analysis completed successfully")
            return (content or "").strip()
        except Exception as e:
            logger.error(f"Error analyzing logs: {e}")
            raise
