import google.generativeai as genai
from app.config import settings
from app.core.logging import logger
# CHANGE: Imported Dict
from typing import Optional, Dict 

class AIService:
    def __init__(self):
        """Initialize AI service with Gemini"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.AI_MODEL)
            logger.info("AI Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI service: {e}")
            self.model = None
    
    # CHANGE: Added optional data argument
    async def generate_insights(self, query: str, context: Optional[dict] = None, data: Optional[Dict] = None) -> str:
        """Generate insights from query using AI"""
        if not self.model:
            return "AI service is currently unavailable. Please check the GEMINI_API_KEY."
        
        try:
            # CHANGE: Pass data to build_prompt
            prompt = self._build_prompt(query, context, data)
            response = self.model.generate_content(prompt)
            
            logger.info(f"Generated insights for query: {query[:50]}...")
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return f"Error: Unable to generate insights. {str(e)}"
    
    # CHANGE: Added optional data argument
    def _build_prompt(self, query: str, context: Optional[dict] = None, data: Optional[Dict] = None) -> str:
        """Build comprehensive prompt for AI"""
        base_prompt = f"""
You are an expert data analyst for agricultural and environmental data.
Analyze the following query and provide detailed, actionable insights.

Query: {query}
"""
        # NEW: Include data snapshot in the prompt if provided
        if data:
            base_prompt += f"\n--- Data Snapshot for Context ---\n{data}\n----------------------------------\n"

        if context:
            base_prompt += f"\nAdditional Context: {context}\n"
        
        base_prompt += """
Guidelines:
1. Provide data-driven analysis with specific numbers when possible
2. Structure your response with headers and bullet points

Analysis:
"""
        return base_prompt

ai_service = AIService()