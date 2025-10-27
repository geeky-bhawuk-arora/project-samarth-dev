import time
import uuid
from typing import Optional, Dict
from app.services.ai_service import ai_service
from app.services.data_service import data_service
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
            
            # Step 1: Fetch relevant data (Now active, currently mocked in data_service.py)
            data = await data_service.fetch_agricultural_data("crop_production", filters)
            
            # Step 2: Generate insights using AI
            # CHANGE: Pass the fetched data to the AI service
            insights = await ai_service.generate_insights(query, context, data)
            
            # Step 3: Format response
            execution_time = time.time() - start_time
            
            return AnalyticsResponse(
                query_id=query_id,
                query=query,
                insights=insights,
                # CHANGE: Extract the list of data points from the dict returned by data_service
                data_points=data.get('data') if data else None,
                execution_time=round(execution_time, 2)
            )
            
        except Exception as e:
            logger.error(f"Error processing query {query_id}: {e}")
            # Re-raise to be caught by the FastAPI router
            raise

query_processor = QueryProcessor()