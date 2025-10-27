from fastapi import APIRouter, HTTPException
from app.models.request_models import AnalyticsQuery, QueryFeedback
from app.models.response_models import AnalyticsResponse, APIResponse
from app.services.query_processor import query_processor
from app.core.logging import logger

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

# Store query history temporarily in memory for POC
query_history = []

@router.post("/query", response_model=AnalyticsResponse)
async def execute_query(query_request: AnalyticsQuery):
    """Execute analytics query and return AI-Powered insights"""
    
    try:
        result = await query_processor.process_query(
            query=query_request.query,
            context=query_request.context,
            filters=query_request.filters
        )
        
        # Store in history
        query_history.append(result.dict())
        
        return result
        
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/history")
async def get_query_history(limit: int = 10):
    """Get recent query history"""
    return {
        "success": True,
        "data": query_history[-limit:],
        "total": len(query_history)
    }

@router.post("/feedback", response_model=APIResponse)
async def submit_feedback(feedback: QueryFeedback):
    """Submit feedback for a query"""
    logger.info(f"Received feedback for query {feedback.query_id}: {feedback.rating}/5")
    
    return APIResponse(
        success=True,
        message="Feedback submitted successfully"
    )