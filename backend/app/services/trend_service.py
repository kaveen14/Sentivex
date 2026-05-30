from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.db_models import Feedback, Prediction, Source

_PERIOD_DAYS: dict[str, int] = {"1d": 1, "7d": 7, "30d": 30, "90d": 90}


def get_trend_data(
    db: Session, period: str = "7d", source: Optional[str] = None
) -> dict:
    days = _PERIOD_DAYS.get(period, 7)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    query = (
        db.query(
            func.date(Prediction.predicted_at).label("bucket"),
            Prediction.sentiment,
            func.count().label("count"),
        )
        .join(Feedback, Feedback.id == Prediction.feedback_id)
        .filter(Prediction.predicted_at >= since)
    )

    if source:
        query = (
            query.join(Source, Source.id == Feedback.source_id)
            .filter(Source.name == source)
        )

    rows = (
        query.group_by("bucket", Prediction.sentiment)
        .order_by("bucket")
        .all()
    )

    timeline_map: dict[str, dict] = {}
    summary: dict[str, int] = {"positive": 0, "neutral": 0, "negative": 0}

    for row in rows:
        date_str = str(row.bucket)
        if date_str not in timeline_map:
            timeline_map[date_str] = {
                "date": date_str,
                "positive": 0,
                "neutral": 0,
                "negative": 0,
            }
        key = row.sentiment.lower()
        if key in timeline_map[date_str]:
            timeline_map[date_str][key] += row.count
            summary[key] += row.count

    summary["total"] = sum(summary.values())

    return {
        "period": period,
        "summary": summary,
        "timeline": sorted(timeline_map.values(), key=lambda x: x["date"]),
    }


def get_feedback_list(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    sentiment: Optional[str] = None,
    source: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> dict:
    query = db.query(Feedback).outerjoin(
        Prediction, Prediction.feedback_id == Feedback.id
    )

    if sentiment:
        query = query.filter(Prediction.sentiment == sentiment)
    if source:
        query = (
            query.join(Source, Source.id == Feedback.source_id)
            .filter(Source.name == source)
        )
    if from_date:
        query = query.filter(Feedback.created_at >= from_date)
    if to_date:
        query = query.filter(Feedback.created_at <= to_date)

    total = query.count()
    items = (
        query.order_by(Feedback.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {"items": items, "total": total, "page": page, "page_size": page_size}
