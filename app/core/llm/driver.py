"""GPT-4o driver for generating buyer persona replies."""

import json
import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

from app.core.persona.prompts import build_driver_messages
from app.core.logs.analyser import LogAnalyser
from app.config.logger import get_logger

if TYPE_CHECKING:
    from app.config.types import Turn

logger = get_logger(__name__)


class LLMDriver:
    """Uses OpenAI GPT-4o to generate persona replies."""

    def __init__(self, model: str, api_key_env: str = "OPENAI_API_KEY"):
        self.model = model
        api_key = os.environ.get(api_key_env)
        if not api_key:
            logger.error(f"Missing {api_key_env} environment variable")
            raise ValueError(f"Missing {api_key_env} environment variable")
        self._client = OpenAI(api_key=api_key)
        logger.info("LLMDriver initialized")

    def generate_reply(
        self,
        persona: dict,
        last_assistant: str,
        recent_turns: list["Turn"],
    ) -> str:
        """Generate the next user (buyer) message given persona and conversation."""
        messages = build_driver_messages(persona, last_assistant, recent_turns)
        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=100,
                temperature=0.4,
            )
            content = resp.choices[0].message.content
            logger.info("Generated reply successfully")
            return (content or "").strip()
        except Exception as e:
            logger.error(f"Error generating reply: {e}")
            raise
