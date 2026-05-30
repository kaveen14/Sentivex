import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, Text, DateTime, ForeignKey, JSON, Uuid
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "sources"

    id = Column(Uuid(as_uuid=True, native_uuid=False), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    type = Column(String(50), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    feedbacks = relationship("Feedback", back_populates="source")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Uuid(as_uuid=True, native_uuid=False), primary_key=True, default=uuid.uuid4)
    source_id = Column(Uuid(as_uuid=True, native_uuid=False), ForeignKey("sources.id"), nullable=True)
    raw_text = Column(Text, nullable=False)
    cleaned_text = Column(Text, nullable=True)
    language = Column(String(10), default="en", nullable=False)
    metadata_ = Column("metadata", JSON, default=dict, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    source = relationship("Source", back_populates="feedbacks")
    prediction = relationship("Prediction", back_populates="feedback", uselist=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Uuid(as_uuid=True, native_uuid=False), primary_key=True, default=uuid.uuid4)
    feedback_id = Column(
        Uuid(as_uuid=True, native_uuid=False), ForeignKey("feedback.id"), nullable=False
    )
    sentiment = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    score_positive = Column(Float, nullable=False)
    score_neutral = Column(Float, nullable=False)
    score_negative = Column(Float, nullable=False)
    model_version = Column(String(50), default="bert-base-uncased-v1", nullable=False)
    predicted_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    feedback = relationship("Feedback", back_populates="prediction")
