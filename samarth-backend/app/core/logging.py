import logging
import sys
import os
from pathlib import Path
from app.config import settings

def setup_logging(log_level: str = settings.LOG_LEVEL):
    """Configure application logging (Vercel-safe)"""

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handlers = [logging.StreamHandler(sys.stdout)]

    # ✅ Check if running on Vercel (read-only filesystem)
    if not os.getenv("VERCEL"):
        # Local or other environments → can write logs
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_path = log_dir / "app.log"
    else:
        # On Vercel → use /tmp if needed
        file_path = Path("/tmp/app.log")

    try:
        handlers.append(logging.FileHandler(file_path))
    except (OSError, PermissionError):
        # Fall back to console-only logging if file can't be created
        pass

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format=log_format,
        handlers=handlers
    )

    return logging.getLogger(__name__)


logger = setup_logging()
