import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import { api } from "@/lib/api";

// Note: install axios-mock-adapter: npm i -D axios-mock-adapter
const mock = new MockAdapter(api);

afterEach(() => mock.reset());

describe("api client — /analyze", () => {
  it("returns sentiment response on success", async () => {
    const payload = {
      id: "abc-123",
      sentiment: "Positive",
      confidence: 0.95,
      scores: { positive: 0.95, neutral: 0.03, negative: 0.02 },
      timestamp: "2026-05-29T10:00:00Z",
    };
    mock.onPost("/analyze").reply(200, payload);

    const res = await api.post("/analyze", { text: "Great product!" });
    expect(res.data.sentiment).toBe("Positive");
    expect(res.data.confidence).toBeCloseTo(0.95);
  });

  it("throws on 422 for empty text", async () => {
    mock.onPost("/analyze").reply(422, { detail: "text must not be empty" });
    await expect(api.post("/analyze", { text: "" })).rejects.toThrow();
  });

  it("throws on 503 when model not ready", async () => {
    mock.onPost("/analyze").reply(503, { detail: "Model is not ready yet." });
    await expect(api.post("/analyze", { text: "test" })).rejects.toThrow();
  });
});

describe("api client — /trends", () => {
  it("returns trend data", async () => {
    const payload = {
      period: "7d",
      summary: { positive: 100, neutral: 30, negative: 10, total: 140 },
      timeline: [],
    };
    mock.onGet("/trends").reply(200, payload);

    const res = await api.get("/trends", { params: { period: "7d" } });
    expect(res.data.period).toBe("7d");
    expect(res.data.summary.total).toBe(140);
  });
});

describe("api client — /health", () => {
  it("returns ok status", async () => {
    mock.onGet("/health").reply(200, { status: "ok", model_loaded: true, version: "1.0.0" });
    const res = await api.get("/health");
    expect(res.data.status).toBe("ok");
    expect(res.data.model_loaded).toBe(true);
  });
});
