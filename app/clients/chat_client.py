"""SSE chat client for the production real-estate agent endpoint."""

import json
from typing import TYPE_CHECKING, Optional, Any
import requests

from app.config.logger import get_logger

if TYPE_CHECKING:
    from app.config.types import ChatResult

logger = get_logger(__name__)


class ChatClient:
    """Client for the production chat SSE endpoint."""

    def __init__(self, api_url: str, user_id: str, timeout_sec: int, retry_count: int):
        self.api_url = api_url
        self.user_id = user_id
        self.timeout_sec = timeout_sec
        self.retry_count = retry_count
        logger.info("ChatClient initialized")

    def send_message(self, content: str, session_id: Optional[str]) -> "ChatResult":
        """Send a message and stream the response. Retries on failure."""
        last_error = None
        for attempt in range(self.retry_count):
            try:
                body = {
                    "userId": self.user_id,
                    "content": content,
                    "stream": True,
                }
                if session_id is not None:
                    body["session_id"] = session_id
                resp = requests.post(
                    self.api_url,
                    json=body,
                    stream=True,
                    timeout=self.timeout_sec,
                    headers={"Accept": "text/event-stream"},
                )
                resp.raise_for_status()
                logger.info(f"Message sent successfully on attempt {attempt + 1}")
                return self._parse_sse(resp)
            except Exception as e:
                last_error = e
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                continue
        logger.error("send_message failed after retries")
        raise last_error or RuntimeError("send_message failed after retries")

    def _parse_sse(self, response: requests.Response) -> "ChatResult":
        """Parse SSE stream and accumulate assistant text and session_id."""
        from app.config.types import ChatResult

        assistant_parts: list[str] = []
        session_id: Optional[str] = None
        raw_events_count = 0
        done = False

        for line in response.iter_lines(decode_unicode=True):
            if line is None:
                continue
            line = line.strip()
            if not line.startswith("data:"):
                continue
            raw_events_count += 1
            payload = line[5:].strip()
            if payload == "[DONE]" or payload == "":
                continue
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                continue
            if not isinstance(data, dict):
                continue
            if data.get("type") == "done":
                done = True
                break
            if "session_id" in data:
                session_id = data["session_id"] or session_id
            delta = ""
            if data.get("type") == "content":
                delta = data.get("delta") or data.get("text") or ""
            else:
                delta = data.get("delta") or ""
            if delta:
                assistant_parts.append(delta if isinstance(delta, str) else str(delta))

        assistant_text = "".join(assistant_parts)
        logger.info(f"Parsed SSE response with {raw_events_count} events")
        return ChatResult(
            assistant_text=assistant_text,
            session_id=session_id,
            raw_events_count=raw_events_count,
        )
