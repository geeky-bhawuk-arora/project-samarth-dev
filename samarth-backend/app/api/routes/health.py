from fastapi import APIRouter
from app.models.response_models import HealthResponse
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        services={
            "api": "operational",
            # Check if Gemini model was initialized
            "ai_service": "operational" if ai_service.model else "unavailable (Check GEMINI_API_KEY)", 
            "database": "mocked" 
        }
    )