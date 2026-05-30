import pytest
import torch
from unittest.mock import MagicMock, patch

from nlp.utils import SENTIMENT_LABELS


class TestBERTSentimentClassifier:
    """Unit tests for the model architecture (mocks HuggingFace download)."""

    def _make_model(self):
        """Create a BERTSentimentClassifier with a mocked BERT backbone."""
        import torch.nn as nn
        from ml.model import BERTSentimentClassifier

        with patch("transformers.BertModel.from_pretrained") as mock_bert_cls:
            mock_bert = MagicMock()
            mock_bert.config.hidden_size = 768
            mock_bert_cls.return_value = mock_bert
            model = BERTSentimentClassifier.__new__(BERTSentimentClassifier)
            nn.Module.__init__(model)
            model.bert = mock_bert
            model.dropout = nn.Dropout(0.3)
            model.classifier = nn.Linear(768, 3)
            model.eval()
        return model

    def test_forward_output_shape_batch_1(self):
        model = self._make_model()
        mock_output = MagicMock()
        mock_output.pooler_output = torch.randn(1, 768)
        model.bert.return_value = mock_output

        ids = torch.randint(0, 1000, (1, 128))
        mask = torch.ones(1, 128, dtype=torch.long)

        with torch.no_grad():
            logits = model(ids, mask)

        assert logits.shape == (1, 3)

    def test_forward_output_shape_batch_4(self):
        model = self._make_model()
        mock_output = MagicMock()
        mock_output.pooler_output = torch.randn(4, 768)
        model.bert.return_value = mock_output

        ids = torch.randint(0, 1000, (4, 64))
        mask = torch.ones(4, 64, dtype=torch.long)

        with torch.no_grad():
            logits = model(ids, mask)

        assert logits.shape == (4, 3)

    def test_classifier_is_linear_768_to_3(self):
        model = self._make_model()
        assert model.classifier.in_features == 768
        assert model.classifier.out_features == 3


class TestSoftmaxProperties:
    def test_softmax_sums_to_one(self):
        logits = torch.tensor([[2.0, 1.0, 0.5], [-1.0, 0.0, 3.0]])
        probs = torch.softmax(logits, dim=1)
        assert torch.allclose(probs.sum(dim=1), torch.ones(2), atol=1e-6)

    def test_argmax_selects_highest_prob_positive(self):
        probs = torch.tensor([[0.05, 0.10, 0.85]])  # idx 2 = Positive
        assert int(probs.argmax(dim=1).item()) == 2
        assert SENTIMENT_LABELS[2] == "Positive"

    def test_argmax_selects_highest_prob_negative(self):
        probs = torch.tensor([[0.80, 0.15, 0.05]])  # idx 0 = Negative
        assert int(probs.argmax(dim=1).item()) == 0
        assert SENTIMENT_LABELS[0] == "Negative"

    def test_confidence_equals_max_prob(self):
        scores = [0.05, 0.10, 0.85]
        pred_idx = scores.index(max(scores))
        assert round(scores[pred_idx], 4) == pytest.approx(0.85, abs=0.001)


class TestSentimentService:
    def test_predict_returns_all_keys(self):
        from app.services.sentiment import SentimentService

        service = SentimentService()
        service.model_loaded = True

        mock_model = MagicMock()
        # Return logits [neg, neu, pos] — positive is dominant
        mock_model.return_value = torch.tensor([[0.05, 0.10, 2.50]])
        service._model = mock_model

        mock_tokenizer = MagicMock()
        mock_tokenizer.encode.return_value = {
            "input_ids": torch.randint(0, 1000, (1, 10)),
            "attention_mask": torch.ones(1, 10, dtype=torch.long),
        }
        service._tokenizer = mock_tokenizer

        mock_preprocessor = MagicMock()
        mock_preprocessor.preprocess.return_value = "great product"
        service._preprocessor = mock_preprocessor

        result = service.predict("Great product!")

        assert "sentiment" in result
        assert "confidence" in result
        assert "scores" in result
        assert set(result["scores"].keys()) == {"positive", "neutral", "negative"}

    def test_predict_scores_sum_to_one(self):
        from app.services.sentiment import SentimentService

        service = SentimentService()
        service.model_loaded = True

        mock_model = MagicMock()
        mock_model.return_value = torch.tensor([[1.0, 0.5, 0.2]])
        service._model = mock_model

        mock_tokenizer = MagicMock()
        mock_tokenizer.encode.return_value = {
            "input_ids": torch.randint(0, 1000, (1, 10)),
            "attention_mask": torch.ones(1, 10, dtype=torch.long),
        }
        service._tokenizer = mock_tokenizer

        mock_preprocessor = MagicMock()
        mock_preprocessor.preprocess.return_value = "decent service"
        service._preprocessor = mock_preprocessor

        result = service.predict("Decent service")
        total = sum(result["scores"].values())
        assert total == pytest.approx(1.0, abs=0.01)

    def test_predict_raises_when_not_loaded(self):
        from app.services.sentiment import SentimentService

        service = SentimentService()
        service.model_loaded = False

        with pytest.raises(RuntimeError, match="not loaded"):
            service.predict("any text")

    def test_predict_label_mapping(self):
        """Verify label indices align with SENTIMENT_LABELS."""
        assert SENTIMENT_LABELS[0] == "Negative"
        assert SENTIMENT_LABELS[1] == "Neutral"
        assert SENTIMENT_LABELS[2] == "Positive"
