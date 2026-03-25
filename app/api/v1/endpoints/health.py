import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/health", tags=["Health"])

logger = logging.getLogger(__name__)


@router.get("")
async def health_check() -> dict:
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check(
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        logger.error("Database health check failed: %s", str(e))
        return {"status": "not_ready", "database": "disconnected"}
