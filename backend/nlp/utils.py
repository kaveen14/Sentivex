import re

# ── Compiled patterns ────────────────────────────────────────────────────────
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
HTML_ENTITY_PATTERN = re.compile(r"&[a-zA-Z]+;|&#\d+;")
MULTIPLE_SPACES_PATTERN = re.compile(r"\s+")
EMOJI_PATTERN = re.compile(
    "[\U00010000-\U0010FFFF"
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE,
)

# ── Label maps ───────────────────────────────────────────────────────────────
SENTIMENT_LABELS: dict[int, str] = {0: "Negative", 1: "Neutral", 2: "Positive"}
LABEL_TO_IDX: dict[str, int] = {"Negative": 0, "Neutral": 1, "Positive": 2}
