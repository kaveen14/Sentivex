import logging
import os

import torch
import torch.nn as nn

logger = logging.getLogger(__name__)

_NUM_LABELS = 3
_MODEL_NAME = "bert-base-uncased"


class BERTSentimentClassifier(nn.Module):
    """3-class BERT-based sentiment classifier (Negative / Neutral / Positive)."""

    def __init__(
        self,
        model_name: str = _MODEL_NAME,
        num_labels: int = _NUM_LABELS,
        dropout: float = 0.3,
    ) -> None:
        super().__init__()
        from transformers import BertModel  # type: ignore

        self.bert = BertModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)

    def forward(
        self, input_ids: torch.Tensor, attention_mask: torch.Tensor
    ) -> torch.Tensor:
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled = outputs.pooler_output          # [batch, 768]
        pooled = self.dropout(pooled)
        return self.classifier(pooled)            # [batch, 3]

    def save(self, path: str) -> None:
        os.makedirs(path, exist_ok=True)
        torch.save(self.state_dict(), os.path.join(path, "model_weights.pt"))
        self.bert.config.save_pretrained(path)
        logger.info("Model saved to %s", path)

    @classmethod
    def load(cls, path: str, device: str = "cpu") -> "BERTSentimentClassifier":
        model = cls()
        weights = os.path.join(path, "model_weights.pt")
        model.load_state_dict(torch.load(weights, map_location=device))
        model.to(device)
        model.eval()
        logger.info("Model loaded from %s", path)
        return model
