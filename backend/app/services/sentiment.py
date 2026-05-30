import logging
import os

from nlp.preprocessor import TextPreprocessor
from nlp.utils import SENTIMENT_LABELS

logger = logging.getLogger(__name__)

_MODEL_PATH = os.getenv("MODEL_PATH", "./models/bert-sentiment")
_FALLBACK_MODEL = "bert-base-uncased"

# ── Torch/Transformers are optional for local dev ────────────────────────────
try:
    import torch
    from nlp.tokenizer import BERTTokenizerWrapper
    _TORCH_AVAILABLE = True
except ImportError:  # pragma: no cover
    _TORCH_AVAILABLE = False
    logger.warning(
        "torch/transformers not installed. Running in RULE-BASED dev mode. "
        "Install with: pip install torch transformers"
    )


# ── Simple keyword-based fallback (no GPU/download needed) ───────────────────
_POSITIVE_WORDS = {
    "great", "excellent", "amazing", "fantastic", "love", "perfect", "good",
    "best", "awesome", "happy", "wonderful", "outstanding", "brilliant",
    "superb", "pleased", "recommend", "satisfied", "impressive", "fast",
}
_NEGATIVE_WORDS = {
    "terrible", "awful", "bad", "horrible", "worst", "hate", "poor", "slow",
    "broken", "damaged", "useless", "disappointed", "failure", "wrong",
    "difficult", "annoying", "refused", "never", "waste", "expensive",
}


def _rule_based_predict(cleaned_text: str) -> dict:
    words = set(cleaned_text.split())
    pos_hits = len(words & _POSITIVE_WORDS)
    neg_hits = len(words & _NEGATIVE_WORDS)

    if pos_hits > neg_hits:
        s, c = "Positive", min(0.5 + pos_hits * 0.1, 0.95)
        scores = {"positive": c, "neutral": round((1 - c) / 2, 4), "negative": round((1 - c) / 2, 4)}
    elif neg_hits > pos_hits:
        s, c = "Negative", min(0.5 + neg_hits * 0.1, 0.95)
        scores = {"negative": c, "neutral": round((1 - c) / 2, 4), "positive": round((1 - c) / 2, 4)}
    else:
        s, c = "Neutral", 0.60
        scores = {"neutral": 0.60, "positive": 0.20, "negative": 0.20}

    return {"sentiment": s, "confidence": round(c, 4), "scores": scores}


class SentimentService:
    """Loads BERT at startup when available; falls back to rule-based for dev."""

    def __init__(self) -> None:
        self._model = None
        self._tokenizer = BERTTokenizerWrapper() if _TORCH_AVAILABLE else None
        self._preprocessor = TextPreprocessor()
        self._device = "cuda" if (_TORCH_AVAILABLE and torch.cuda.is_available()) else "cpu"
        self.model_loaded = False
        self._use_rules = not _TORCH_AVAILABLE

    async def load_model(self) -> None:
        if not _TORCH_AVAILABLE:
            logger.info("Dev mode: rule-based sentiment classifier active.")
            self.model_loaded = True
            return

        from ml.model import BERTSentimentClassifier

        self._tokenizer.load()
        weights = os.path.join(_MODEL_PATH, "model_weights.pt")

        if os.path.isdir(_MODEL_PATH) and os.path.exists(weights):
            self._model = BERTSentimentClassifier.load(_MODEL_PATH, self._device)
            logger.info("Fine-tuned BERT loaded from %s.", _MODEL_PATH)
        else:
            logger.warning(
                "No fine-tuned weights at %s — loading base BERT (untrained). "
                "Run ml/trainer.py to fine-tune.",
                _MODEL_PATH,
            )
            self._model = BERTSentimentClassifier(_FALLBACK_MODEL).to(self._device)
            self._model.eval()

        self.model_loaded = True

    def predict(self, text: str) -> dict:
        """Classify a single text. Returns sentiment, confidence, scores."""
        if not self.model_loaded:
            raise RuntimeError("Model is not loaded.")

        cleaned = self._preprocessor.preprocess(text)

        # ── Rule-based dev mode ──────────────────────────────────────────────
        if self._use_rules or self._model is None:
            result = _rule_based_predict(cleaned)
            result["cleaned_text"] = cleaned
            return result

        # ── BERT inference ───────────────────────────────────────────────────
        enc = self._tokenizer.encode(cleaned, device=self._device)
        with torch.no_grad():
            logits = self._model(
                input_ids=enc["input_ids"],
                attention_mask=enc["attention_mask"],
            )
            probs = torch.softmax(logits, dim=1).squeeze()

        scores = probs.cpu().numpy().tolist()
        pred_idx = int(probs.argmax().item())

        return {
            "sentiment": SENTIMENT_LABELS[pred_idx],
            "confidence": round(scores[pred_idx], 4),
            "scores": {
                "negative": round(scores[0], 4),
                "neutral": round(scores[1], 4),
                "positive": round(scores[2], 4),
            },
            "cleaned_text": cleaned,
        }

    def predict_batch(self, texts: list[str]) -> list[dict]:
        return [self.predict(t) for t in texts]
