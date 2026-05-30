import pytest
from nlp.preprocessor import TextPreprocessor


@pytest.fixture
def preprocessor() -> TextPreprocessor:
    return TextPreprocessor()


class TestPreprocessorHappyPath:
    def test_basic_text(self, preprocessor):
        assert preprocessor.preprocess("The product is great!") == "the product is great!"

    def test_lowercases(self, preprocessor):
        assert preprocessor.preprocess("AMAZING PRODUCT") == "amazing product"

    def test_normalizes_whitespace(self, preprocessor):
        result = preprocessor.preprocess("too    many   spaces")
        assert "  " not in result

    def test_strips_html_tags(self, preprocessor):
        result = preprocessor.preprocess("<p>Great <b>product</b>!</p>")
        assert "<" not in result and ">" not in result
        assert "great" in result

    def test_strips_urls_http(self, preprocessor):
        result = preprocessor.preprocess("Visit https://example.com for details")
        assert "https" not in result
        assert "example.com" not in result

    def test_strips_urls_www(self, preprocessor):
        result = preprocessor.preprocess("See www.example.com for more")
        assert "www.example.com" not in result

    def test_decodes_amp_entity(self, preprocessor):
        result = preprocessor.preprocess("Good &amp; fast")
        assert "&amp;" not in result
        assert "&" in result

    def test_decodes_lt_gt_entities(self, preprocessor):
        result = preprocessor.preprocess("&lt;script&gt;alert(1)&lt;/script&gt;")
        assert "&lt;" not in result and "&gt;" not in result

    def test_strips_emojis(self, preprocessor):
        result = preprocessor.preprocess("Great product 😊🎉🔥")
        assert "😊" not in result
        assert "🎉" not in result
        assert "great product" in result

    def test_handles_mixed_html_and_emoji(self, preprocessor):
        result = preprocessor.preprocess("<div>Excellent 🌟</div>")
        assert "<" not in result
        assert "excellent" in result

    def test_strips_nested_html(self, preprocessor):
        result = preprocessor.preprocess("<div><span>Hello</span> <a href='#'>World</a></div>")
        assert "hello" in result and "world" in result
        assert "<" not in result

    def test_long_text_is_processed(self, preprocessor):
        long_text = "good product " * 300
        result = preprocessor.preprocess(long_text)
        assert len(result) > 0


class TestPreprocessorEdgeCases:
    def test_raises_on_empty_string(self, preprocessor):
        with pytest.raises(ValueError, match="empty"):
            preprocessor.preprocess("")

    def test_raises_on_whitespace_only(self, preprocessor):
        with pytest.raises(ValueError):
            preprocessor.preprocess("   \t\n  ")

    def test_raises_when_html_strips_all_content(self, preprocessor):
        with pytest.raises(ValueError):
            preprocessor.preprocess("<p>   </p>")

    def test_preserves_punctuation_for_sentiment(self, preprocessor):
        result = preprocessor.preprocess("Not good at all!")
        assert "!" in result

    def test_nbsb_entity_stripped(self, preprocessor):
        result = preprocessor.preprocess("Hello&nbsp;World")
        assert "&nbsp;" not in result
        assert "hello" in result


class TestLanguageDetection:
    def test_detect_language_english(self, preprocessor):
        lang = preprocessor.detect_language("This is an English sentence.")
        assert lang == "en"

    def test_is_english_returns_bool(self, preprocessor):
        result = preprocessor.is_english("The weather is nice today.")
        assert isinstance(result, bool)
