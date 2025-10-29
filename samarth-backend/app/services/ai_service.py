import google.generativeai as genai
from app.config import settings
from app.core.logging import logger
from app.tools.sql_tools import SQL_TOOL, get_db_schema
from typing import Optional

class AIService:
    def __init__(self):
        """Initialize AI service with Gemini configuration"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model_name = settings.AI_MODEL
            self.system_instruction = self._get_system_instruction()

            # ✅ Attach system instruction when creating the model
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=self.system_instruction,
                tools=[SQL_TOOL],  # Attach tools once at model level
            )

            logger.info(f"AI Service initialized successfully with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize AI service: {e}")
            self.model = None

    def _get_system_instruction(self) -> str:
        schema = get_db_schema()
        return f"""
You are the Project Samarth Cross-Domain Data Analyst.
Your job is to analyze data using SQL and summarize relationships clearly.
Database schema:
{schema}
"""

    async def generate_insights(self, query: str, context: Optional[dict] = None) -> str:
        """Runs full Text-to-SQL → Execution → Synthesis pipeline."""
        if not self.model:
            return "AI service is currently unavailable. Please check the GEMINI_API_KEY."

        try:
            # 1️⃣ Generate initial content
            response = self.model.generate_content(
                query,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.4,   # optional fine-tuning params
                    top_p=0.9,
                    max_output_tokens=1024,
                )
            )

            # 2️⃣ Handle Tool Calls
            while hasattr(response, "function_calls") and response.function_calls:
                tool_outputs = []
                for call in response.function_calls:
                    if call.name == SQL_TOOL.__name__:
                        sql_query = call.args.get("query", "")
                        logger.info(f"[AGENT ACTION] Executing PostgreSQL SQL: {sql_query}")
                        result = SQL_TOOL(sql_query)
                        tool_outputs.append({
                            "role": "function",
                            "name": call.name,
                            "content": {"result": result},
                        })

                # Feed tool results back to the model
                response = self.model.generate_content(
                    [
                        {"role": "user", "parts": [query]},
                        *tool_outputs
                    ]
                )

            logger.info(f"Generated insights for query: {query[:60]}...")

            # Safely extract textual content from the response. The library's
            # `response.text` property will raise when any non-text parts
            # (e.g. function_call) are present. Build the text from text parts
            # as a robust fallback.
            def _extract_text_from_response(resp) -> str:
                try:
                    # preferred path when response is all-text
                    return resp.text
                except Exception:
                    texts = []
                    # the response may expose `parts` which contain typed parts
                    parts = getattr(resp, "parts", None)
                    if parts:
                        for p in parts:
                            # parts can be objects or dict-like
                            t = None
                            if hasattr(p, "text"):
                                t = p.text
                            elif isinstance(p, dict) and "text" in p:
                                t = p.get("text")
                            # Some parts represent assistant messages with nested
                            # 'content' or 'message' shapes — try common keys
                            if not t and isinstance(p, dict):
                                for key in ("content", "message", "body"):
                                    if key in p and isinstance(p[key], str):
                                        t = p[key]
                                        break
                            if t:
                                texts.append(t)
                    # final fallback to string representation
                    joined = "\n".join(texts).strip()
                    return joined or str(resp)

            return _extract_text_from_response(response)

        except Exception as e:
            logger.error(f"Error during agent execution: {e}", exc_info=True)
            if "API_KEY" in str(e):
                return "Error: Gemini API Key is missing or invalid."
            return f"Error: Unable to generate insights. {str(e)}"


ai_service = AIService()
