"use client";

import { useState } from "react";
import { useFeedback } from "@/lib/hooks/useFeedback";
import { FeedbackTable } from "@/components/tables/FeedbackTable";

const SENTIMENTS = ["", "Positive", "Neutral", "Negative"];

export default function ExplorerPage() {
  const [sentiment, setSentiment] = useState("");
  const [page, setPage] = useState(1);

  const { data, isLoading, isError } = useFeedback({
    sentiment: sentiment || undefined,
    page,
    pageSize: 20,
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Data Explorer</h1>

      {/* Filters */}
      <div className="flex gap-3 items-center">
        <label className="text-sm text-gray-400">Filter by sentiment:</label>
        <select
          value={sentiment}
          onChange={(e) => { setSentiment(e.target.value); setPage(1); }}
          className="bg-gray-800 text-gray-200 rounded-lg px-3 py-1.5 text-sm border border-gray-700"
        >
          {SENTIMENTS.map((s) => (
            <option key={s} value={s}>{s || "All"}</option>
          ))}
        </select>
      </div>

      {isLoading && <p className="text-gray-400 animate-pulse">Loading…</p>}
      {isError && <p className="text-red-400">Failed to load feedback.</p>}

      {data && (
        <>
          <FeedbackTable items={data.items} />
          {/* Pagination */}
          <div className="flex items-center gap-4 text-sm text-gray-400">
            <button
              disabled={page <= 1}
              onClick={() => setPage((p) => p - 1)}
              className="px-3 py-1 bg-gray-800 rounded-lg disabled:opacity-40"
            >
              Prev
            </button>
            <span>Page {page} · {data.total} total</span>
            <button
              disabled={page * 20 >= data.total}
              onClick={() => setPage((p) => p + 1)}
              className="px-3 py-1 bg-gray-800 rounded-lg disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}
