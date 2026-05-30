import logging
from typing import Union

import torch

logger = logging.getLogger(__name__)

_MODEL_NAME = "bert-base-uncased"
_MAX_LENGTH = 512


class BERTTokenizerWrapper:
    """Thin wrapper around HuggingFace BertTokenizerFast."""

    def __init__(self, model_name: str = _MODEL_NAME) -> None:
        self.model_name = model_name
        self._tokenizer = None

    def load(self) -> None:
        from transformers import BertTokenizerFast  # type: ignore

        logger.info("Loading tokenizer: %s", self.model_name)
        self._tokenizer = BertTokenizerFast.from_pretrained(self.model_name)
        logger.info("Tokenizer loaded.")

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            self.load()
        return self._tokenizer

    def encode(self, text: Union[str, list[str]], device: str = "cpu") -> dict:
        """
        Tokenize one or more texts.

        Returns:
            Dict of tensors (input_ids, attention_mask) placed on `device`.
        """
        texts = [text] if isinstance(text, str) else text
        encoded = self.tokenizer(
            texts,
            max_length=_MAX_LENGTH,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )
        return {k: v.to(device) for k, v in encoded.items()}
