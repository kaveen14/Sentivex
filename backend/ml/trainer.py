import logging
import os

import torch
from sklearn.model_selection import train_test_split
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from transformers import get_linear_schedule_with_warmup  # type: ignore

from ml.model import BERTSentimentClassifier
from nlp.preprocessor import TextPreprocessor
from nlp.tokenizer import BERTTokenizerWrapper

logger = logging.getLogger(__name__)


class SentimentDataset(Dataset):
    def __init__(self, encodings: dict, labels: list[int]) -> None:
        self.encodings = encodings
        self.labels = labels

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> dict:
        item = {k: v[idx] for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item


class SentimentTrainer:
    """Fine-tunes BERTSentimentClassifier on a labelled CSV dataset."""

    def __init__(
        self,
        model_name: str = "bert-base-uncased",
        output_dir: str = "models/bert-sentiment",
        epochs: int = 10,
        batch_size: int = 16,
        lr: float = 2e-5,
        patience: int = 3,
    ) -> None:
        self.model_name = model_name
        self.output_dir = output_dir
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr
        self.patience = patience
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._preprocessor = TextPreprocessor()
        self._tokenizer = BERTTokenizerWrapper(model_name)
        self._tokenizer.load()

    def train(
        self, csv_path: str, text_col: str = "text", label_col: str = "label"
    ) -> None:
        """
        Fine-tune on a CSV.
        Expected columns: `text` (str), `label` (int: 0=Neg, 1=Neu, 2=Pos).
        """
        import pandas as pd

        df = pd.read_csv(csv_path)
        texts = [self._preprocessor.preprocess(t) for t in df[text_col].tolist()]
        labels = df[label_col].tolist()

        tr_texts, val_texts, tr_labels, val_labels = train_test_split(
            texts, labels, test_size=0.15, stratify=labels, random_state=42
        )

        tr_enc = self._tokenizer.encode(tr_texts)
        val_enc = self._tokenizer.encode(val_texts)

        tr_loader = DataLoader(
            SentimentDataset(tr_enc, tr_labels),
            batch_size=self.batch_size,
            shuffle=True,
        )
        val_loader = DataLoader(
            SentimentDataset(val_enc, val_labels),
            batch_size=self.batch_size * 2,
        )

        model = BERTSentimentClassifier(self.model_name).to(self.device)
        optimizer = AdamW(model.parameters(), lr=self.lr, weight_decay=0.01)
        total_steps = len(tr_loader) * self.epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=total_steps // 10,
            num_training_steps=total_steps,
        )
        criterion = torch.nn.CrossEntropyLoss()

        best_val_loss = float("inf")
        no_improve = 0

        for epoch in range(1, self.epochs + 1):
            model.train()
            tr_loss = 0.0
            for batch in tr_loader:
                ids = batch["input_ids"].to(self.device)
                mask = batch["attention_mask"].to(self.device)
                lbl = batch["labels"].to(self.device)

                optimizer.zero_grad()
                logits = model(ids, mask)
                loss = criterion(logits, lbl)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()
                tr_loss += loss.item()

            avg_tr = tr_loss / len(tr_loader)
            avg_val = self._eval_loss(model, val_loader, criterion)
            logger.info("Epoch %d  train=%.4f  val=%.4f", epoch, avg_tr, avg_val)

            if avg_val < best_val_loss:
                best_val_loss = avg_val
                no_improve = 0
                model.save(self.output_dir)
                logger.info("Best model saved.")
            else:
                no_improve += 1
                if no_improve >= self.patience:
                    logger.info("Early stopping at epoch %d.", epoch)
                    break

    def _eval_loss(self, model, loader, criterion) -> float:
        model.eval()
        total = 0.0
        with torch.no_grad():
            for batch in loader:
                ids = batch["input_ids"].to(self.device)
                mask = batch["attention_mask"].to(self.device)
                lbl = batch["labels"].to(self.device)
                total += criterion(model(ids, mask), lbl).item()
        return total / len(loader)
