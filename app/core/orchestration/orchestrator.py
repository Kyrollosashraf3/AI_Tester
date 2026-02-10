"""Orchestrator: run the conversation loop until summary or limits."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from app.config.types import RunReport, Turn
from app.config.settings import LOGS_API_URL, LOGS_LIMIT, USER_ID

from app.core.persona.persona import persona_context, is_question, stop_condition

from app.clients.logs_client import LogsApiClient
from app.core.logs.reader import LogsReader
from app.core.logs.analyser import LogAnalyser

from app.config.logger import get_logger

if TYPE_CHECKING:
    from app.clients.chat_client import ChatClient
    from app.core.llm.driver import LLMDriver

logger = get_logger(__name__)


class Orchestrator:
    """Runs the chat loop: send user message, get assistant, decide next or stop."""

    def __init__(
        self,
        chat: "ChatClient",
        driver: "LLMDriver",
        max_turns: int,
        max_total_seconds: int,
    ):
        self.chat = chat
        self.driver = driver
        self.max_turns = max_turns
        self.max_total_seconds = max_total_seconds
        self.log_analyser = LogAnalyser()
        logger.info("Orchestrator initialized")

    def run(self, initial_user_message: str, initial_real_estate_message: str) -> RunReport:
        """Run the conversation until stop condition or limits."""
        started_at = datetime.utcnow()
        turns: list[Turn] = []
        session_id: Optional[str] = str(uuid4())
        persona = persona_context()
        current_user_message = initial_user_message
        assistant_text = initial_real_estate_message

        # --- NEW: init logs reader once ---
        # reuse chat client's timeout/retry
        timeout_sec = getattr(self.chat, "timeout_sec", 30)
        retry_count = getattr(self.chat, "retry_count", 1)

        logs_client = LogsApiClient(
            logs_api_url=LOGS_API_URL,
            timeout_sec=timeout_sec,
            retry_count=retry_count,
        )
        logs_reader = LogsReader(logs_client)

        try:
            for turn_index in range(self.max_turns):

                # If timeout: stop
                elapsed = (datetime.utcnow() - started_at).total_seconds()
                if elapsed >= self.max_total_seconds:
                    logger.error("max_total_seconds exceeded")
                    return RunReport(
                        success=False,
                        user_id = USER_ID,
                        session_id= session_id, 
                        turns=turns,
                        final_summary=None,
                        started_at=started_at,
                        ended_at=datetime.utcnow(),
                        error="max_total_seconds exceeded",
                    )

                # 1) Start Chat real_estate
                turns.append(Turn(role="assistant", user_id=  USER_ID, session_id= session_id,content=assistant_text, ts=datetime.utcnow()))     # why do u need to buy
                turns.append(Turn(role="user",      user_id=  USER_ID, session_id= session_id, content=current_user_message, ts=datetime.utcnow()))     # hello i need ... for stability 

                logger.info(f"real_estate_message = {assistant_text}")
                logger.info(f"Turn {turn_index + 1}: user msg (len={len(current_user_message)})")

                # 4) send message (SSE) >>> Let Response , Take Logs
                result = self.chat.send_message(current_user_message, session_id)  # very good - stability , when > logs
                session_id = result.session_id or session_id

               

                # Update session_id in all existing turns
                for turn in turns:
                    turn.session_id = session_id

                
                # return : new response from real estate , with result LOGS   
                # take logs to analysis now ,, then take this response in next turn

                # 2) --- read logs for THIS message only ---
                # We rely on cursor-by-max-id. Since session starts new (session_id=None),
                # first call should safely return logs for first message too, so prime_if_first_time=False.
                try:
                    user_id = getattr(self.chat, "user_id", None)
                    if user_id and session_id:
                        new_logs = logs_reader.get_logs(
                            user_id=user_id,
                            session_id=session_id,
                            limit=LOGS_LIMIT,
                            prime_if_first_time=False if turn_index == 0 else True,
                        )

                except Exception as e:
                    logger.error(f"Failed to read logs: {e}")

                # 3) check logs
                """new logs : json -- send it to llm with last user message and real_estate response """
                report_logs = self.log_analyser.analyse(last_assistant=assistant_text, user_response=current_user_message, logs=new_logs)

                logger.info(f"report_logs: {report_logs}")

                # 4) send message (SSE)  NOW take the response
                assistant_text = result.assistant_text.strip()   # very good - stability , when
                
                turns[-1].logs_report = report_logs

                # 4) determine if response is Q or stop
                is_q = is_question(assistant_text)
                stopped = stop_condition(assistant_text)
                logger.info(
                    f"assistant len={len(assistant_text)}, is_question={is_q}, "
                    f"stop_condition={stopped}, session_id={session_id}"
                )

                if stopped:
                     return RunReport(success=True,
                                        user_id = USER_ID,
                                        session_id= session_id, 
                                        turns=turns, 
                                        final_summary=assistant_text,
                                        started_at=started_at,
                                        ended_at=datetime.utcnow(),error=None,)

                
                if is_q:      # if true   > generate new user message , give it to current_user_message
                    recent = turns[-10:] if len(turns) >= 10 else turns
                    current_user_message = self.driver.generate_reply(persona, assistant_text, recent)     # 6 months

                    if not current_user_message:
                        current_user_message = "I'm not sure what to say."
                else:
                    current_user_message = "Okay."

                logger.info(f"final message to new turn--- current_user_message: {current_user_message}")

            logger.info("max_turns exceeded")
            return RunReport(
                success=True,
                user_id = USER_ID,
                session_id= session_id,
                turns=turns,
                final_summary=None,
                started_at=started_at,
                ended_at=datetime.utcnow(),
                error="max_turns exceeded",
            )
        except Exception as e:
            logger.error(f"Exception in run: {e}")
            return RunReport(
                success=False,
                user_id = USER_ID,
                session_id= session_id,
                turns=turns,
                final_summary=None,
                started_at=started_at,
                ended_at=datetime.utcnow(),
                error=str(e),
            )
