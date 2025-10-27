from pydantic import BaseModel, Field
from typing import Optional

class AnalyticsQuery(BaseModel):
    query: str = Field(..., min_length=10, max_length=1000)
    context: Optional[dict] = None
    filters: Optional[dict] = None

class QueryFeedback(BaseModel):
    query_id: str
    rating: int = Field(..., ge=1, le=5)
    feedback: Optional[str] = None