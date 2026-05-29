"use client";

import { useFeedback } from "@/lib/hooks/useFeedback";

export default function IssuesPage() {
  const { data, isLoading, isError } = useFeedback({ sentiment: "Negative", pageSize: 20 });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Issue Detection</h1>
      <p className="text-gray-400 text-sm">
        Showing the most recent negative feedback entries.
      </p>

      {isLoading && <p className="text-gray-400 animate-pulse">Loading…</p>}
      {isError && <p className="text-red-400">Failed to load issue data.</p>}

      {data && (
        <div className="space-y-3">
          {data.items.length === 0 && (
            <p className="text-gray-500">No negative feedback found.</p>
          )}
          {data.items.map((item) => (
            <div
              key={item.id}
              className="bg-gray-900 rounded-xl p-4 border-l-4 border-red-500"
            >
              <p className="text-sm text-gray-200">{item.raw_text}</p>
              <div className="flex gap-4 mt-2 text-xs text-gray-500">
                {item.source && <span>Source: {item.source}</span>}
                {item.confidence !== null && item.confidence !== undefined && (
                  <span>Confidence: {(item.confidence * 100).toFixed(0)}%</span>
                )}
                <span>{new Date(item.created_at).toLocaleString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
