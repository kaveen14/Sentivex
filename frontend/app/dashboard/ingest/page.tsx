"use client";

import { useState } from "react";
import { api } from "@/lib/api";

interface Result {
  sentiment: string;
  confidence: number;
  scores: { positive: number; neutral: number; negative: number };
}

const SENTIMENT_COLOR: Record<string, string> = {
  Positive: "text-green-400",
  Neutral: "text-yellow-400",
  Negative: "text-red-400",
};

export default function IngestPage() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.post<Result>("/analyze", { text });
      setResult(res.data);
    } catch {
      setError("Analysis failed. Check the API is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-2xl font-bold">Manual Feedback Ingest</h1>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste customer feedback here…"
        rows={5}
        className="w-full bg-gray-900 border border-gray-700 rounded-xl p-4 text-sm text-gray-200 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />

      <button
        onClick={handleAnalyze}
        disabled={loading || !text.trim()}
        className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 rounded-lg font-medium transition-colors"
      >
        {loading ? "Analysing…" : "Analyse Sentiment"}
      </button>

      {error && <p className="text-red-400 text-sm">{error}</p>}

      {result && (
        <div className="bg-gray-900 rounded-xl p-5 space-y-3">
          <p className="text-sm text-gray-400">Result</p>
          <p className={`text-3xl font-bold ${SENTIMENT_COLOR[result.sentiment] ?? ""}`}>
            {result.sentiment}
          </p>
          <p className="text-sm text-gray-400">
            Confidence: <span className="text-white">{(result.confidence * 100).toFixed(1)}%</span>
          </p>
          <div className="flex gap-6 text-sm">
            <span className="text-green-400">Positive: {(result.scores.positive * 100).toFixed(1)}%</span>
            <span className="text-yellow-400">Neutral: {(result.scores.neutral * 100).toFixed(1)}%</span>
            <span className="text-red-400">Negative: {(result.scores.negative * 100).toFixed(1)}%</span>
          </div>
        </div>
      )}
    </div>
  );
}
