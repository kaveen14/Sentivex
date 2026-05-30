import logging

import torch
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from torch.utils.data import DataLoader

from ml.model import BERTSentimentClassifier
from ml.trainer import SentimentDataset
from nlp.preprocessor import TextPreprocessor
from nlp.tokenizer import BERTTokenizerWrapper
from nlp.utils import SENTIMENT_LABELS

logger = logging.getLogger(__name__)


def evaluate_model(
    model_path: str,
    csv_path: str,
    text_col: str = "text",
    label_col: str = "label",
) -> dict:
    """Evaluate a saved model on a test CSV and return a metrics dict."""
    import pandas as pd

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = BERTSentimentClassifier.load(model_path, device)

    preprocessor = TextPreprocessor()
    tokenizer = BERTTokenizerWrapper()
    tokenizer.load()

    df = pd.read_csv(csv_path)
    texts = [preprocessor.preprocess(t) for t in df[text_col].tolist()]
    true_labels = df[label_col].tolist()

    encodings = tokenizer.encode(texts, device=device)
    dataset = SentimentDataset(encodings, true_labels)
    loader = DataLoader(dataset, batch_size=32)

    preds: list[int] = []
    model.eval()
    with torch.no_grad():
        for batch in loader:
            logits = model(
                batch["input_ids"].to(device),
                batch["attention_mask"].to(device),
            )
            preds.extend(torch.argmax(logits, dim=1).cpu().numpy().tolist())

    return {
        "accuracy": accuracy_score(true_labels, preds),
        "macro_f1": f1_score(true_labels, preds, average="macro"),
        "precision_per_class": precision_score(
            true_labels, preds, average=None
        ).tolist(),
        "recall_per_class": recall_score(true_labels, preds, average=None).tolist(),
        "confusion_matrix": confusion_matrix(true_labels, preds).tolist(),
        "label_map": SENTIMENT_LABELS,
    }
