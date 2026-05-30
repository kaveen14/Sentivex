from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import db_models, schemas
from app.services.sentiment import SentimentService

router = APIRouter(tags=["Analysis"])
limiter = Limiter(key_func=get_remote_address)


def _get_service(request: Request) -> SentimentService:
    return request.app.state.sentiment_service


@router.post("/analyze", response_model=schemas.AnalyzeResponse)
@limiter.limit("100/minute")
async def analyze_feedback(
    request: Request,
    body: schemas.AnalyzeRequest,
    db: Session = Depends(get_db),
    service: SentimentService = Depends(_get_service),
):
    if not service.model_loaded:
        raise HTTPException(status_code=503, detail="Model is not ready yet.")

    result = service.predict(body.text)

    feedback = db_models.Feedback(
        raw_text=body.text,
        cleaned_text=result["cleaned_text"],
        language="en",
        metadata_=body.metadata or {},
    )
    db.add(feedback)
    db.flush()

    prediction = db_models.Prediction(
        feedback_id=feedback.id,
        sentiment=result["sentiment"],
        confidence=result["confidence"],
        score_positive=result["scores"]["positive"],
        score_neutral=result["scores"]["neutral"],
        score_negative=result["scores"]["negative"],
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return schemas.AnalyzeResponse(
        id=prediction.id,
        sentiment=prediction.sentiment,
        confidence=prediction.confidence,
        scores=schemas.SentimentScores(**result["scores"]),
        timestamp=prediction.predicted_at,
    )


@router.post("/analyze/batch", response_model=schemas.BatchAnalyzeResponse)
@limiter.limit("20/minute")
async def analyze_batch(
    request: Request,
    body: schemas.BatchAnalyzeRequest,
    db: Session = Depends(get_db),
    service: SentimentService = Depends(_get_service),
):
    if not service.model_loaded:
        raise HTTPException(status_code=503, detail="Model is not ready yet.")

    responses = []
    for item in body.items:
        result = service.predict(item.text)

        feedback = db_models.Feedback(
            raw_text=item.text,
            cleaned_text=result["cleaned_text"],
            language="en",
            metadata_=item.metadata or {},
        )
        db.add(feedback)
        db.flush()

        prediction = db_models.Prediction(
            feedback_id=feedback.id,
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            score_positive=result["scores"]["positive"],
            score_neutral=result["scores"]["neutral"],
            score_negative=result["scores"]["negative"],
        )
        db.add(prediction)
        db.flush()

        responses.append(
            schemas.AnalyzeResponse(
                id=prediction.id,
                sentiment=prediction.sentiment,
                confidence=prediction.confidence,
                scores=schemas.SentimentScores(**result["scores"]),
                timestamp=prediction.predicted_at,
            )
        )

    db.commit()
    return schemas.BatchAnalyzeResponse(results=responses, total=len(responses))
