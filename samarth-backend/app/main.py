from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.core.logging import logger, setup_logging
from app.api.routes import health, analytics

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting Project Samarth API...")
    yield
    logger.info("Shutting down Project Samarth API...")

app = FastAPI(
    title="Project Samarth API",
    description="AI-Powered Agricultural Data Analytics Core Functionality",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analytics.router)

@app.get("/")
async def root():
    return {
        "service": "Project Samarth API",
        "version": "1.0.0",
        "status": "operational (POC)",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )