import time
import uuid
from typing import Optional, Dict
from app.services.ai_service import ai_service
# Removed data_service import as it is no longer used for fetching data
from app.core.logging import logger
from app.models.response_models import AnalyticsResponse

class QueryProcessor:
    """Process analytics queries end-to-end"""
    
    async def process_query(
        self,
        query: str,
        context: Optional[Dict] = None,
        filters: Optional[Dict] = None
    ) -> AnalyticsResponse:
        """Process analytics query and return insights"""
        
        query_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            logger.info(f"Processing query {query_id}: {query[:50]}...")
            
            # Data fetching is now handled internally by the AI Agent via SQL Tool.
            
            insights = await ai_service.generate_insights(query, context)
            
            execution_time = time.time() - start_time
            
            return AnalyticsResponse(
                query_id=query_id,
                query=query,
                insights=insights,
                data_points=None, # Data points are embedded in the 'insights' string
                execution_time=round(execution_time, 2)
            )
            
        except Exception as e:
            logger.error(f"Error processing query {query_id}: {e}")
            raise # Re-raise to be caught by the FastAPI router

query_processor = QueryProcessor()
