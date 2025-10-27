import logging
import sys
from pathlib import Path
from app.config import settings

def setup_logging(log_level: str = settings.LOG_LEVEL):
    """Configure application logging"""
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "app.log")
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()