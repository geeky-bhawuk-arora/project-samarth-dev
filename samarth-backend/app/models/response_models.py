from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    timestamp: datetime = datetime.utcnow()

class AnalyticsResponse(BaseModel):
    query_id: str
    query: str
    insights: str
    data_points: Optional[List[dict]] = None
    execution_time: float
    timestamp: datetime = datetime.utcnow()

class HealthResponse(BaseModel):
    status: str
    version: str
    services: dict
    timestamp: datetime = datetime.utcnow()