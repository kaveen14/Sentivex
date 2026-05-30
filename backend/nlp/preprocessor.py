import logging
from nlp.utils import (
    HTML_TAG_PATTERN,
    URL_PATTERN,
    HTML_ENTITY_PATTERN,
    MULTIPLE_SPACES_PATTERN,
    EMOJI_PATTERN,
)

logger = logging.getLogger(__name__)

try:
    from langdetect import detect, LangDetectException  # type: ignore
    _LANGDETECT_AVAILABLE = True
except ImportError:
    _LANGDETECT_AVAILABLE = False
    logger.warning("langdetect not installed; language detection disabled.")

_HTML_ENTITIES: dict[str, str] = {
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
    "&quot;": '"',
    "&#39;": "'",
    "&nbsp;": " ",
}


class TextPreprocessor:
    """Cleans and normalises raw customer feedback text for BERT input."""

    def preprocess(self, text: str) -> str:
        """
        Full preprocessing pipeline.

        Raises:
            ValueError: If text is empty or becomes empty after cleaning.
        """
        if not text or not text.strip():
            raise ValueError("Input text is empty.")

        text = self._strip_html(text)
        text = self._strip_urls(text)
        text = self._decode_html_entities(text)
        text = self._strip_emojis(text)
        text = text.lower()
        text = self._normalize_whitespace(text)

        result = text.strip()
        if not result:
            raise ValueError("Text is empty after preprocessing.")
        return result

    def detect_language(self, text: str) -> str:
        if not _LANGDETECT_AVAILABLE:
            return "en"
        try:
            return detect(text)
        except Exception:
            return "unknown"

    def is_english(self, text: str) -> bool:
        return self.detect_language(text) == "en"

    # ── private helpers ──────────────────────────────────────────────────────

    def _strip_html(self, text: str) -> str:
        return HTML_TAG_PATTERN.sub(" ", text)

    def _strip_urls(self, text: str) -> str:
        return URL_PATTERN.sub(" ", text)

    def _decode_html_entities(self, text: str) -> str:
        for entity, char in _HTML_ENTITIES.items():
            text = text.replace(entity, char)
        return HTML_ENTITY_PATTERN.sub(" ", text)

    def _strip_emojis(self, text: str) -> str:
        return EMOJI_PATTERN.sub(" ", text)

    def _normalize_whitespace(self, text: str) -> str:
        return MULTIPLE_SPACES_PATTERN.sub(" ", text)
