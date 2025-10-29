import google.generativeai as genai
from google.generativeai import types
from app.config import settings
from app.core.logging import logger
from app.tools.sql_tools import SQL_TOOL, get_db_schema # Import the Postgres tool and schema
from typing import Optional, Dict

class AIService:
    def __init__(self):
        """Initialize AI service with Gemini"""
        try:
            # Using the correct environment variable name from settings
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = settings.AI_MODEL
            logger.info(f"AI Service initialized successfully with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize AI service: {e}")
            self.model = None

    def _get_system_instruction(self) -> str:
        """Define the LLM Agent's persona, goal, and the PostgreSQL data schema."""
        schema = get_db_schema()
        
        return f"""
You are the Project Samarth Cross-Domain Data Analyst. Your goal is to answer complex, natural language queries by synthesizing data from the unified PostgreSQL data store.

Your process MUST be:
1.  **Analyze & Plan:** Determine all numerical data points needed (e.g., averages, sums, specific records) to answer the query.
2.  **Generate SQL:** Call the `execute_mock_sql` tool ONCE with a single, highly-optimized SQL query that retrieves ALL necessary raw data. Use standard PostgreSQL SQL dialect. The table name is agri_climate_data.
3.  **Execute & Observe:** The tool will execute and return a JSON result containing the data.
4.  **Synthesize & Reason (Cross-Domain):** Use the retrieved numerical facts to calculate metrics and derive the final *cross-domain insight* (e.g., correlate rainfall trend vs. production).
5.  **Final Answer:** Present the answer in a professional, natural language summary. **Cite the specific data points/calculations** from the SQL result to back up your conclusions.

--- DATABASE SCHEMA (PostgreSQL) ---
{schema}
---

NEVER output raw SQL or data outside of the tool call/response.
"""

    async def generate_insights(self, query: str, context: Optional[dict] = None) -> str:
        """Runs the full LLM agent workflow: NL -> Text-to-SQL -> Execution -> Synthesis."""
        if not self.model:
            return "AI service is currently unavailable. Please check the GEMINI_API_KEY."

        client = genai.Client()
        system_instruction = self._get_system_instruction()
        
        contents = [types.Content(role="user", parts=[types.Part.from_text(query)])]

        try:
            # 1. Initial call: LLM generates a tool call (SQL query)
            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=system_instruction),
                tools=[SQL_TOOL] 
            )

            # 2. Check for Tool Calls and Execute (Multi-turn synthesis loop)
            while response.function_calls:
                tool_calls = response.function_calls
                tool_outputs = []

                for call in tool_calls:
                    if call.name == SQL_TOOL.__name__:
                        sql_query = call.args.get("query", "")
                        logger.info(f"[AGENT ACTION] Executing PostgreSQL SQL: {sql_query}")
                        
                        # Execute the tool (SQL_TOOL is synchronous)
                        output = SQL_TOOL(sql_query)
                        
                        tool_outputs.append(
                            types.Part.from_function_response(
                                name=call.name,
                                response={ "result": output }
                            )
                        )
                
                # Append history and tool output
                contents.append(response.candidates[0].content)
                contents.extend(tool_outputs)
                
                # 3. Second call: LLM synthesizes the final answer
                response = client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=types.GenerateContentConfig(system_instruction=system_instruction),
                    tools=[SQL_TOOL]
                )
                
            logger.info(f"Generated insights for query: {query[:50]}...")
            return response.text

        except Exception as e:
            logger.error(f"Error during agent execution: {e}")
            if "API_KEY" in str(e):
                return "Error: Gemini API Key is missing or invalid. Check your environment configuration."
            return f"Error: Unable to generate insights. An internal error occurred. {str(e)}"

ai_service = AIService()
