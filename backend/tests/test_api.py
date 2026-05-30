import pytest


class TestHealthEndpoint:
    def test_returns_200(self, client):
        res = client.get("/api/v1/health")
        assert res.status_code == 200

    def test_response_shape(self, client):
        data = client.get("/api/v1/health").json()
        assert data["status"] == "ok"
        assert data["model_loaded"] is True
        assert "version" in data


class TestAnalyzeSingle:
    def test_valid_text_returns_200(self, client):
        res = client.post("/api/v1/analyze", json={"text": "This product is absolutely fantastic!"})
        assert res.status_code == 200

    def test_response_contains_required_fields(self, client):
        data = client.post("/api/v1/analyze", json={"text": "Excellent service."}).json()
        assert "id" in data
        assert "sentiment" in data
        assert "confidence" in data
        assert "scores" in data
        assert "timestamp" in data

    def test_scores_contain_all_classes(self, client):
        scores = client.post("/api/v1/analyze", json={"text": "Good product."}).json()["scores"]
        assert set(scores.keys()) == {"positive", "neutral", "negative"}

    def test_accepts_source_field(self, client):
        res = client.post(
            "/api/v1/analyze",
            json={"text": "Great support!", "source": "support_ticket"},
        )
        assert res.status_code == 200

    def test_accepts_metadata_field(self, client):
        res = client.post(
            "/api/v1/analyze",
            json={"text": "Fast delivery.", "metadata": {"region": "US"}},
        )
        assert res.status_code == 200

    def test_rejects_empty_text(self, client):
        assert client.post("/api/v1/analyze", json={"text": ""}).status_code == 422

    def test_rejects_whitespace_text(self, client):
        assert client.post("/api/v1/analyze", json={"text": "   "}).status_code == 422

    def test_rejects_missing_text_field(self, client):
        assert client.post("/api/v1/analyze", json={"source": "crm"}).status_code == 422

    def test_rejects_text_over_10000_chars(self, client):
        assert (
            client.post("/api/v1/analyze", json={"text": "x" * 10_001}).status_code == 422
        )

    def test_model_not_ready_returns_503(self, client, mock_service):
        mock_service.model_loaded = False
        res = client.post("/api/v1/analyze", json={"text": "Hello!"})
        assert res.status_code == 503
        mock_service.model_loaded = True  # restore


class TestAnalyzeBatch:
    def test_batch_two_items(self, client):
        res = client.post(
            "/api/v1/analyze/batch",
            json={"items": [{"text": "Good!"}, {"text": "Bad."}]},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["total"] == 2
        assert len(data["results"]) == 2

    def test_batch_single_item(self, client):
        res = client.post(
            "/api/v1/analyze/batch",
            json={"items": [{"text": "Average experience."}]},
        )
        assert res.status_code == 200

    def test_batch_rejects_empty_list(self, client):
        assert (
            client.post("/api/v1/analyze/batch", json={"items": []}).status_code == 422
        )

    def test_batch_rejects_over_100_items(self, client):
        items = [{"text": f"item {i}"} for i in range(101)]
        assert (
            client.post("/api/v1/analyze/batch", json={"items": items}).status_code == 422
        )


class TestTrendsEndpoint:
    def test_returns_200(self, client):
        assert client.get("/api/v1/trends").status_code == 200

    def test_default_period_is_7d(self, client):
        data = client.get("/api/v1/trends").json()
        assert data["period"] == "7d"

    def test_all_valid_periods(self, client):
        for p in ("1d", "7d", "30d", "90d"):
            assert client.get(f"/api/v1/trends?period={p}").status_code == 200

    def test_summary_has_all_keys(self, client):
        summary = client.get("/api/v1/trends").json()["summary"]
        assert {"positive", "neutral", "negative", "total"}.issubset(summary.keys())

    def test_timeline_is_list(self, client):
        timeline = client.get("/api/v1/trends").json()["timeline"]
        assert isinstance(timeline, list)


class TestFeedbackEndpoint:
    def test_returns_200(self, client):
        assert client.get("/api/v1/feedback").status_code == 200

    def test_response_has_pagination_fields(self, client):
        data = client.get("/api/v1/feedback").json()
        assert {"items", "total", "page", "page_size"}.issubset(data.keys())

    def test_page_size_param(self, client):
        data = client.get("/api/v1/feedback?page=1&page_size=5").json()
        assert data["page_size"] == 5

    def test_sentiment_filter_param(self, client):
        res = client.get("/api/v1/feedback?sentiment=Positive")
        assert res.status_code == 200

    def test_items_is_list(self, client):
        data = client.get("/api/v1/feedback").json()
        assert isinstance(data["items"], list)
