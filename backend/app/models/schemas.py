from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10_000)
    source: Optional[str] = Field(default="manual", max_length=100)
    metadata: Optional[dict] = Field(default_factory=dict)

    @field_validator("text")
    @classmethod
    def text_not_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be empty or whitespace only")
        return v


class SentimentScores(BaseModel):
    positive: float
    neutral: float
    negative: float


class AnalyzeResponse(BaseModel):
    id: UUID
    sentiment: str
    confidence: float
    scores: SentimentScores
    timestamp: datetime

    model_config = {"from_attributes": True}


class BatchAnalyzeRequest(BaseModel):
    items: list[AnalyzeRequest] = Field(..., min_length=1, max_length=100)


class BatchAnalyzeResponse(BaseModel):
    results: list[AnalyzeResponse]
    total: int


class FeedbackItem(BaseModel):
    id: UUID
    raw_text: str
    sentiment: Optional[str] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class FeedbackListResponse(BaseModel):
    items: list[FeedbackItem]
    total: int
    page: int
    page_size: int


class TrendDataPoint(BaseModel):
    date: str
    positive: int
    neutral: int
    negative: int


class TrendSummary(BaseModel):
    positive: int
    neutral: int
    negative: int
    total: int


class TrendResponse(BaseModel):
    period: str
    summary: TrendSummary
    timeline: list[TrendDataPoint]


class HealthResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    status: str
    model_loaded: bool
    version: str
