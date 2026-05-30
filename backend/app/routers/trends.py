from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.schemas import (
    FeedbackItem,
    FeedbackListResponse,
    HealthResponse,
    TrendResponse,
)
from app.services.trend_service import get_feedback_list, get_trend_data

router = APIRouter(tags=["Trends & Data"])


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    service = getattr(request.app.state, "sentiment_service", None)
    return HealthResponse(
        status="ok",
        model_loaded=service.model_loaded if service else False,
        version="1.0.0",
    )


@router.get("/trends", response_model=TrendResponse)
async def get_trends(
    period: str = "7d",
    source: Optional[str] = None,
    db: Session = Depends(get_db),
):
    data = get_trend_data(db, period=period, source=source)
    return TrendResponse(**data)


@router.get("/feedback", response_model=FeedbackListResponse)
async def list_feedback(
    page: int = 1,
    page_size: int = 20,
    sentiment: Optional[str] = None,
    source: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    result = get_feedback_list(
        db,
        page=page,
        page_size=min(page_size, 100),
        sentiment=sentiment,
        source=source,
        from_date=from_date,
        to_date=to_date,
    )

    items = []
    for fb in result["items"]:
        pred = fb.prediction
        items.append(
            FeedbackItem(
                id=fb.id,
                raw_text=fb.raw_text,
                sentiment=pred.sentiment if pred else None,
                confidence=pred.confidence if pred else None,
                source=fb.source.name if fb.source else None,
                created_at=fb.created_at,
            )
        )

    return FeedbackListResponse(
        items=items,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )
