import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.db_models import Base, Feedback, Prediction, Source


@pytest.fixture(scope="module")
def db_engine():
    eng = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)


@pytest.fixture
def session(db_engine):
    Session = sessionmaker(bind=db_engine)
    s = Session()
    yield s
    s.rollback()
    s.close()


class TestSourceModel:
    def test_create_source(self, session):
        src = Source(name="test_source", type="review")
        session.add(src)
        session.commit()
        result = session.query(Source).filter_by(name="test_source").first()
        assert result is not None
        assert result.type == "review"

    def test_default_active_is_true(self, session):
        src = Source(name="active_src", type="ticket")
        session.add(src)
        session.commit()
        assert src.active is True

    def test_id_is_assigned(self, session):
        src = Source(name="id_src", type="email")
        session.add(src)
        session.commit()
        assert src.id is not None

    def test_created_at_is_set(self, session):
        src = Source(name="ts_src", type="crm")
        session.add(src)
        session.commit()
        assert src.created_at is not None


class TestFeedbackModel:
    def test_create_feedback(self, session):
        fb = Feedback(raw_text="Great product!", cleaned_text="great product!", language="en")
        session.add(fb)
        session.commit()
        result = session.query(Feedback).filter_by(raw_text="Great product!").first()
        assert result is not None
        assert result.language == "en"

    def test_created_at_is_set(self, session):
        fb = Feedback(raw_text="Test entry")
        session.add(fb)
        session.commit()
        assert fb.created_at is not None

    def test_metadata_defaults_to_dict(self, session):
        fb = Feedback(raw_text="Another entry")
        session.add(fb)
        session.commit()
        assert isinstance(fb.metadata_, dict)

    def test_feedback_without_source(self, session):
        fb = Feedback(raw_text="No source here")
        session.add(fb)
        session.commit()
        assert fb.source_id is None

    def test_feedback_id_is_assigned(self, session):
        fb = Feedback(raw_text="ID test")
        session.add(fb)
        session.commit()
        assert fb.id is not None


class TestPredictionModel:
    def test_create_prediction(self, session):
        fb = Feedback(raw_text="Prediction test feedback")
        session.add(fb)
        session.flush()

        pred = Prediction(
            feedback_id=fb.id,
            sentiment="Positive",
            confidence=0.95,
            score_positive=0.95,
            score_neutral=0.03,
            score_negative=0.02,
        )
        session.add(pred)
        session.commit()

        result = session.query(Prediction).filter_by(feedback_id=fb.id).first()
        assert result is not None
        assert result.sentiment == "Positive"

    def test_confidence_value(self, session):
        fb = Feedback(raw_text="Confidence test")
        session.add(fb)
        session.flush()

        pred = Prediction(
            feedback_id=fb.id,
            sentiment="Neutral",
            confidence=0.72,
            score_positive=0.10,
            score_neutral=0.72,
            score_negative=0.18,
        )
        session.add(pred)
        session.commit()
        assert pred.confidence == pytest.approx(0.72, abs=0.001)

    def test_prediction_feedback_relationship(self, session):
        fb = Feedback(raw_text="Relationship test")
        session.add(fb)
        session.flush()

        pred = Prediction(
            feedback_id=fb.id,
            sentiment="Negative",
            confidence=0.88,
            score_positive=0.05,
            score_neutral=0.07,
            score_negative=0.88,
        )
        session.add(pred)
        session.commit()
        session.refresh(fb)

        assert fb.prediction is not None
        assert fb.prediction.sentiment == "Negative"

    def test_predicted_at_is_set(self, session):
        fb = Feedback(raw_text="Timestamp prediction test")
        session.add(fb)
        session.flush()

        pred = Prediction(
            feedback_id=fb.id,
            sentiment="Positive",
            confidence=0.90,
            score_positive=0.90,
            score_neutral=0.05,
            score_negative=0.05,
        )
        session.add(pred)
        session.commit()
        assert pred.predicted_at is not None

    def test_model_version_default(self, session):
        fb = Feedback(raw_text="Version test")
        session.add(fb)
        session.flush()

        pred = Prediction(
            feedback_id=fb.id,
            sentiment="Neutral",
            confidence=0.60,
            score_positive=0.20,
            score_neutral=0.60,
            score_negative=0.20,
        )
        session.add(pred)
        session.commit()
        assert pred.model_version == "bert-base-uncased-v1"


class TestFeedbackSourceRelationship:
    def test_feedback_linked_to_source(self, session):
        src = Source(name="rel_source", type="review")
        session.add(src)
        session.flush()

        fb = Feedback(raw_text="From review source", source_id=src.id)
        session.add(fb)
        session.commit()
        session.refresh(fb)

        assert fb.source is not None
        assert fb.source.name == "rel_source"
